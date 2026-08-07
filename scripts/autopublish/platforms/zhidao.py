"""Zhidao (百度知道) answerer — Q&A form, no cover image."""
import time
import re
import json
from urllib.parse import quote
from pathlib import Path

from .base import PlatformPublisher


class ZhidaoPublisher(PlatformPublisher):
    """Answers questions on Baidu Zhidao via browser automation.

    Flow (route A — answer an existing high-traffic question):
      1. locate target question via `target_question_url` (manual, required)
      2. click 『我来答』 (#answer-bar)
      3. fill UEditor iframe body (#ueditor_0 body.view)
      4. click 『提交回答』 (.new-editor-deliver-btn)
    No cover image — zhidao answers are text-based.

    DOM verified on 2026-08-07 against real question page.
    """

    # ---- reused helpers (mirrors baijiahao) ----
    def _check_captcha(self) -> bool:
        page = self.engine.page
        url = page.url.lower()
        if any(x in url for x in ["wappass", "passport.baidu.com", "/verify", "captcha"]):
            return True
        selectors = [
            '.verify-pop', '.verify-modal', '.captcha-wrap', '.captcha-modal',
            '.slider', '.geetest', '.TANGRAM__PSP', '.passport-login-pop',
            '.security-verify', '[class*="verify"]', '[class*="captcha"]',
        ]
        for sel in selectors:
            try:
                loc = page.locator(sel).first
                if loc.is_visible(timeout=800):
                    return True
            except Exception:
                pass
        return False

    def _wait_user(self, msg: str):
        self._checkpoint("_user-pause", msg)
        print(f"\n{'='*60}")
        print(f"⏸️  {msg}")
        print(f"   浏览器保持打开，请手动处理，完成后在终端按 Enter")
        print(f"{'='*60}\n")
        input(">>> 按 Enter 继续...")
        self._checkpoint("_user-resumed", "用户处理后")

    @staticmethod
    def _md_to_html(md: str) -> str:
        html = md
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        # Drop URLs entirely — zhidao treats any link as advertising risk
        html = re.sub(r'\[(.+?)\]\((.+?)\)', r'\1', html)
        html = re.sub(r'https?://\S+', '', html)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'\n\n', '<p></p>', html)
        html = re.sub(r'\n', '<br>', html)
        return html

    # ---- main ----
    def publish(self, content: dict, cover_path: str = None):
        engine = self.engine
        page = engine.page
        question = content.get("question") or content.get("title", "")
        answer = content.get("_body", "")
        target_url = content.get("target_question_url", "")

        # === STEP 1: locate target question ===
        print(f"[zhidao] locating question: {question[:30]}...")
        if not target_url:
            print("[zhidao] WARN: target_question_url 为空；百度知道站内搜索易触发滑块验证，")
            print("          请在源稿里填入要回答的真实问题页 URL，或在浏览器中手动打开问题页。")
            self._wait_user("请在浏览器中手动打开要回答的问题页，然后按 Enter")
        else:
            engine.goto(target_url, wait_until="domcontentloaded")
        time.sleep(3)
        self._checkpoint("01-question-page", "问题页已打开")

        if self._check_captcha():
            self._wait_user("检测到安全验证，请手动完成后按 Enter")

        # === STEP 2: click 『写回答』 ===
        print(f"[zhidao] clicking 我来答...")
        write_btn = page.locator("#answer-bar").first
        try:
            write_btn.scroll_into_view_if_needed(timeout=3000)
            time.sleep(0.3)
            write_btn.click(timeout=5000)
            # wait for UEditor root to appear
            page.wait_for_selector(".edui-editor", state="visible", timeout=8000)
        except Exception as e:
            print(f"[zhidao] 我来答 click failed: {e}")
            self._checkpoint("02-write-fail", "未点到我来答")
            self._wait_user("请手动点『我来答』展开编辑器，然后按 Enter")
        time.sleep(2)
        self._checkpoint("02-answer-editor", "回答编辑器已打开")

        # === STEP 3: fill answer box ===
        print(f"[zhidao] filling answer...")
        html_answer = self._md_to_html(answer)
        filled = False
        # UEditor: contenteditable body inside iframe #ueditor_0
        try:
            iframe = page.frame_locator("#ueditor_0")
            body = iframe.locator("body.view")
            body.wait_for(state="visible", timeout=5000)
            # remove init placeholder
            page.evaluate("""
                () => {
                    const iframe = document.getElementById('ueditor_0');
                    if (!iframe || !iframe.contentDocument) return;
                    const init = iframe.contentDocument.getElementById('initContent');
                    if (init) init.remove();
                }
            """)
            # click body and set html
            body.click(timeout=3000)
            time.sleep(0.3)
            # select all & type to mimic human
            page.keyboard.press("Control+A")
            time.sleep(0.2)
            page.keyboard.press("Backspace")
            time.sleep(0.2)
            page.keyboard.type(answer, delay=6)
            filled = True
            print(f"[zhidao] answer typed into UEditor body")
        except Exception as e:
            print(f"[zhidao] UEditor body type failed: {e}")

        # Fallback: set innerHTML directly via JS
        if not filled:
            try:
                page.evaluate("""
                    (html) => {
                        const iframe = document.getElementById('ueditor_0');
                        if (!iframe || !iframe.contentDocument) throw new Error('iframe missing');
                        const bd = iframe.contentDocument.body;
                        bd.innerHTML = html;
                    }
                """, html_answer)
                filled = True
                print(f"[zhidao] answer filled via JS innerHTML fallback")
            except Exception as e:
                print(f"[zhidao] JS innerHTML fallback failed: {e}")

        if not filled:
            self._checkpoint("03-answer-fail", "回答框填写失败")
            self._wait_user("请手动粘贴回答内容，然后按 Enter")
        self._checkpoint("03-answer-filled", "回答已填")

        # === STEP 4: submit ===
        self._checkpoint("04-ready-submit", "准备提交")
        self._wait_user("回答已填写！请检查内容。\n如满意，终端按 Enter 自动点击『提交回答』。")

        print(f"[zhidao] clicking 提交回答...")
        submit_btn = page.locator(".new-editor-deliver-btn").first
        try:
            submit_btn.scroll_into_view_if_needed(timeout=3000)
            time.sleep(0.3)
            submit_btn.click(timeout=8000)
            time.sleep(3)
        except Exception as e:
            print(f"[zhidao] submit failed: {e}")
            self._checkpoint("05-submit-fail", "提交失败")
            self._wait_user("请手动点击『提交回答』")

        if self._check_captcha():
            self._wait_user("提交后出现安全验证，请手动完成")

        self._checkpoint("06-after-submit", "提交后")
        url = page.url
        print(f"[zhidao] Final URL: {url}")
        self._wait_user("提交完成！确认无误后按 Enter 关闭浏览器")
        return {"success": True, "url": url, "title": question}
