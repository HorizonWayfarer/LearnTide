"""Autopublish core engine — Playwright browser automation."""
import os
import sys
import json
import time
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = Path(__file__).resolve().parent / "config.json"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

class BrowserEngine:
    """Launches and controls a Playwright browser with persistent profile."""

    def __init__(self, platform: str = "baijiahao"):
        self.config = load_config()
        self.platform = platform
        profile_key = self.config["profiles"][platform]
        self.profile_dir = str(BASE_DIR / profile_key["profile_dir"])
        Path(self.profile_dir).mkdir(parents=True, exist_ok=True)
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    def start(self, headless: bool = False) -> "BrowserEngine":
        """Start browser. Call this first."""
        self._playwright = sync_playwright().start()
        browser_type = self._playwright.chromium
        self._context = browser_type.launch_persistent_context(
            user_data_dir=self.profile_dir,
            headless=headless,
            viewport={"width": 1280, "height": 800},
            locale="zh-CN",
            slow_mo=300,  # slow down actions to mimic human
        )
        self._page = self._context.pages[0] if self._context.pages else self._context.new_page()
        return self

    @property
    def page(self):
        if self._page is None or self._page.is_closed():
            self._page = self._context.new_page()
        return self._page

    def goto(self, url: str, wait_until: str = "domcontentloaded"):
        self.page.goto(url, wait_until=wait_until, timeout=30000)
        time.sleep(1)

    def type_and_submit(self, selector: str, text: str, timeout: int = 10000):
        try:
            self.page.locator(selector).first.fill(text, timeout=timeout)
        except Exception:
            self.page.locator(selector).first.type(text, timeout=timeout)

    def click(self, selector: str, timeout: int = 10000):
        self.page.locator(selector).first.click(timeout=timeout)

    def wait_for(self, selector: str, timeout: int = 15000):
        self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)

    def screenshot(self, path: str, full_page: bool = False):
        self.page.screenshot(path=path, full_page=full_page)
        return path

    def eval_js(self, script: str):
        return self.page.evaluate(script)

    def stop(self):
        if self._page:
            try:
                self._page.close()
            except:
                pass
        if self._context:
            self._context.close()
        if self._playwright:
            self._playwright.stop()
