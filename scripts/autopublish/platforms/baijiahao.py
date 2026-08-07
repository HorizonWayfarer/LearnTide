"""Baijiahao (百家号) publisher — using data-testid selectors."""
import time
import re
import json
from pathlib import Path

from .base import PlatformPublisher

EDITOR_URL = "https://baijiahao.baidu.com/builder/rc/edit?type=news&is_from_cms=1"


class BaijiahaoPublisher(PlatformPublisher):
    """Publishes articles to Baijiahao via direct editor URL with precise selectors."""

    def _check_captcha(self) -> bool:
        """Detect real captcha/login challenge (visible modal or URL redirect).

        Old implementation scanned body.innerText for keywords like "验证", which
        falsely triggered on normal editor text. Now we only react to:
          - redirect to baidu passport/wappass/verify/captcha URLs
          - visible verification slider/modal elements
        """
        page = self.engine.page
        url = page.url.lower()
        if any(x in url for x in ["wappass", "passport.baidu.com", "/verify", "captcha"]):
            return True

        # common captcha / login-challenge selectors on baidu properties
        selectors = [
            '.verify-pop',
            '.verify-modal',
            '.captcha-wrap',
            '.captcha-modal',
            '.slider',
            '.geetest',
            '.TANGRAM__PSP',
            '.passport-login-pop',
            '.security-verify',
            '[class*="verify"]',
            '[class*="captcha"]',
        ]
        for sel in selectors:
            try:
                loc = page.locator(sel).first
                if loc.is_visible(timeout=800):
                    return True
            except Exception:
                pass
        return False

    def _dismiss_dialogs(self):
        """Close any visible dialog/popover."""
        page = self.engine.page
        try:
            # Look for confirm buttons in dialogs
            dialogs = page.locator('.modal, .dialog, .popconfirm, .bjh-dialog')
            for i in range(dialogs.count()):
                d = dialogs.nth(i)
                if d.is_visible(timeout=1000):
                    # Try to find confirm/close button
                    btns = d.locator('button:has-text("确认"), button:has-text("×"), .close')
                    if btns.count() > 0:
                        btns.first.click(timeout=2000)
                        time.sleep(0.3)
                        print(f"[baijiahao] Dialog dismissed")
                        return True
            return False
        except:
            return False

    def _upload_cover(self, cover_path: str) -> bool:
        """Upload a cover image via the 『选择封面』 dialog.

        Flow (verified against baijiahao editor DOM):
          1. click 『选择封面』 -> opens cheetah-modal with tabs
             『正文/本地上传』(default) / 『AI封图』 / 『免费正版图库』
          2. the dialog contains a dedicated image input[type=file][accept*=image]
             (distinct from the body's video/* input — this was the old bug)
          3. set_input_files on that input; the uploaded image is auto-selected,
             confirm button turns into 『确定 (1)』
          4. click 『确定』 -> dialog closes, cover is set
        """
        page = self.engine.page
        print(f"[baijiahao] Uploading cover: {cover_path}")
        try:
            # 1. open the cover dialog — the cover section is content-driven and
            #    renders only after title/body exist, so poll until it's visible.
            #    Two entry states:
            #      - fresh draft  -> 『选择封面』 (div)
            #      - has a cover  -> 『更换』 button (draft restored / replacing)
            entry = None
            entry_selectors = ['text=选择封面', 'button:has-text("更换")']
            for _ in range(12):
                for sel in entry_selectors:
                    loc = page.locator(sel).first
                    try:
                        if loc.count() > 0 and loc.is_visible(timeout=800):
                            entry = loc
                            print(f"[baijiahao] cover entry via: {sel}")
                            break
                    except Exception:
                        pass
                if entry is not None:
                    break
                time.sleep(1)
            if entry is None:
                print("[baijiahao] cover: entry not visible (cover section not rendered)")
                return False
            try:
                entry.scroll_into_view_if_needed(timeout=3000)
            except Exception:
                pass
            try:
                entry.click(timeout=5000)
            except Exception:
                # JS click fallback in case an overlay intercepts the pointer
                entry.evaluate("el => el.click()")
            time.sleep(2.5)

            # 2. locate the IMAGE file input (accept*=image), never the video one
            img_input = page.locator('input[type="file"][accept*="image"]')
            if img_input.count() == 0:
                print("[baijiahao] cover: image input not found")
                return False
            img_input.first.set_input_files(cover_path)
            print("[baijiahao] cover: file set, waiting for upload...")

            # 3. poll until the confirm button shows a selected count 『确定 (N)』
            #    or an image thumbnail appears — max ~15s
            selected = False
            for _ in range(15):
                time.sleep(1)
                info = page.evaluate("""() => {
                    const modal = document.querySelector('.cheetah-modal-content');
                    if (!modal) return {open: false, ready: false};
                    const btns = Array.from(modal.querySelectorAll('button'))
                        .map(b => (b.textContent||'').trim());
                    const confirm = btns.find(t => t.startsWith('确定'));
                    const hasCount = confirm && /\\(\\s*[1-9]/.test(confirm);
                    const hasImg = modal.querySelector('img[src^="blob:"], img[src*="bdstatic"], img[src*="baidu"]') !== null;
                    return {open: true, ready: !!(hasCount || hasImg), confirm: confirm};
                }""")
                if not info.get("open"):
                    break
                if info.get("ready"):
                    selected = True
                    print(f"[baijiahao] cover: uploaded ({info.get('confirm')})")
                    break

            if not selected:
                print("[baijiahao] cover: upload not confirmed in time")
                return False

            # 4. click 确定
            ok_btn = page.locator('.cheetah-modal-content button:has-text("确定")').first
            ok_btn.click(timeout=5000)
            time.sleep(2.5)

            # verify dialog closed
            still_open = page.evaluate(
                "() => !!document.querySelector('.cheetah-modal-content')?.offsetParent"
            )
            if still_open:
                print("[baijiahao] cover: dialog still open after 确定")
                return False
            print("[baijiahao] cover: done")
            return True
        except Exception as e:
            print(f"[baijiahao] cover upload error: {e}")
            return False

    def _wait_user(self, msg: str):
        self._checkpoint("_user-pause", msg)
        print(f"\n{'='*60}")
        print(f"⏸️  {msg}")
        print(f"   浏览器保持打开，请手动处理，完成后在终端按 Enter")
        print(f"{'='*60}\n")
        input(">>> 按 Enter 继续...")
        self._dismiss_dialogs()
        self._checkpoint("_user-resumed", "用户处理后")

    def publish(self, content: dict, cover_path: str = None):
        engine = self.engine
        page = engine.page
        title = content.get("title", "")
        body = content.get("_body", "")
        topic = content.get("topic", "")

        # === STEP 1: Navigate to editor ===
        print(f"[baijiahao] Navigating to editor...")
        engine.goto(EDITOR_URL, wait_until="domcontentloaded")
        time.sleep(4)
        self._checkpoint("01-editor-loaded", "编辑器已打开")

        if self._check_captcha():
            self._wait_user("检测到安全验证，请手动完成后按 Enter")

        # === STEP 2: Type title ===
        # Selector: data-testid="news-title-input" > [contenteditable="true"]
        print(f"[baijiahao] Filling title: {title[:30]}...")
        title_ok = False
        try:
            # Click the title contenteditable div directly
            title_el = page.locator('[data-testid="news-title-input"] [contenteditable="true"]').first
            title_el.click(timeout=5000)
            time.sleep(0.3)
            # Clear existing content
            page.keyboard.press("Control+A")
            time.sleep(0.2)
            page.keyboard.press("Backspace")
            time.sleep(0.2)
            # Type title - use shorter delay for speed
            page.keyboard.type(title, delay=8)
            print(f"[baijiahao] Title filled ({len(title)} chars)")
            title_ok = True
        except Exception as e:
            print(f"[baijiahao] Title failed: {e}")
            self._checkpoint("02-title-fail", "标题填写失败")
            self._wait_user("请手动在标题框输入标题，然后按 Enter")

        self._checkpoint("02-title-filled", "标题已填")

        # === STEP 3: Fill body ===
        print(f"[baijiahao] Filling body...")
        # The body editor is inside #ueditor which has an iframe
        body_ok = False
        html_body = self._md_to_html(body)

        # Strategy 1: Inject via JS into the ueditor iframe
        try:
            iframe = page.frame_locator('iframe').first
            # Click the iframe body to focus
            iframe.locator('body').first.click(timeout=5000)
            time.sleep(0.3)
            # Inject HTML
            iframe.locator('body').first.evaluate(
                f"document.body.innerHTML = {json.dumps(html_body, ensure_ascii=False)}"
            )
            print(f"[baijiahao] Body injected into iframe")
            body_ok = True
        except Exception as e1:
            print(f"[baijiahao] Body iframe failed: {e1}")
            # Strategy 2: Try the editor div directly
            try:
                editor = page.locator('[contenteditable="true"]').first
                cls = editor.evaluate("el => el.className")
                if "FeEditorApp" in cls:
                    editor.click(timeout=3000)
                    time.sleep(0.3)
                    page.evaluate(
                        """(html) => {
                            var els = document.querySelectorAll('[contenteditable="true"]');
                            for (var i = 0; i < els.length; i++) {
                                if (els[i].className.indexOf("FeEditorApp") >= 0) {
                                    els[i].innerHTML = html;
                                    els[i].dispatchEvent(new Event("input", { bubbles: true }));
                                }
                            }
                        }""",
                        html_body,
                    )
                    body_ok = True
                    print(f"[baijiahao] Body injected into FeEditorApp div")
            except Exception as e2:
                print(f"[baijiahao] Body FeEditorApp failed: {e2}")

        if not body_ok:
            # Strategy 3: Clipboard paste
            try:
                page.evaluate(f"navigator.clipboard.writeText({json.dumps(html_body, ensure_ascii=False)})")
                page.locator('[contenteditable="true"]').first.click(timeout=3000)
                time.sleep(0.3)
                page.keyboard.press("Control+v")
                time.sleep(0.5)
                print(f"[baijiahao] Body pasted via clipboard")
                body_ok = True
            except Exception as e3:
                print(f"[baijiahao] Body clipboard failed: {e3}")

        if not body_ok:
            self._checkpoint("03-body-fail", "正文填写失败")
            self._wait_user("请手动粘贴正文内容，然后按 Enter")

        self._checkpoint("03-body-filled", "正文已填")

        # === STEP 4: Upload cover ===
        if cover_path:
            ok = self._upload_cover(cover_path)
            if ok:
                self._checkpoint("03b-cover-done", "封面已上传")
            else:
                self._checkpoint("03b-cover-fail", "封面上传失败")
                self._wait_user(
                    f"封面自动上传失败，请手动点『选择封面』上传这张图后按 Enter:\n   {cover_path}"
                )

        # === STEP 5: Publish ===
        self._checkpoint("04-ready-publish", "准备发布")
        self._wait_user(
            "内容已填写完毕！请检查标题、正文、封面。\n"
            "如满意，终端按 Enter 自动点击『发布』按钮。"
        )

        print(f"[baijiahao] Clicking publish...")
        try:
            pub_btn = page.locator('button:has-text("发布")').filter(
                has=page.locator('.cheetah-btn-primary')
            )
            if pub_btn.count() == 0:
                pub_btn = page.locator('button:has-text("发布")')

            pub_btn.first.click(timeout=10000)
            print(f"[baijiahao] Publish button clicked")
            time.sleep(4)
        except Exception as e:
            print(f"[baijiahao] Publish failed: {e}")
            self._checkpoint("05-publish-fail", "发布失败")
            self._wait_user("请手动点击浏览器中的『发布』按钮")

        if self._check_captcha():
            self._wait_user("发布后出现安全验证，请手动完成")

        self._checkpoint("06-after-publish", "发布后")
        url = page.url
        print(f"[baijiahao] Final URL: {url}")

        self._wait_user("发布完成！确认无误后按 Enter 关闭浏览器")

        return {"success": True, "url": url, "title": title}

    @staticmethod
    def _md_to_html(md: str) -> str:
        html = md
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'\n\n', '<p></p>', html)
        html = re.sub(r'\n', '<br>', html)
        return html
