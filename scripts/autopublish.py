#!/usr/bin/env python3
"""
Autopublish CLI — 自动发布到内容平台。

Usage:
    python scripts/autopublish.py list                    # 列出待发布文章
    python scripts/autopublish.py publish baijiahao      # 发布百家号文章
    python scripts/autopublish.py publish baijiahao 0    # 发布百家号第1篇
    python scripts/autopublish.py login baijiahao        # 启动浏览器等你登录
"""
import sys
import os
import json
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from autopublish.core import BrowserEngine, load_config
from autopublish.content import get_pending, parse_front_matter
from autopublish.cover_fetcher import search_cover
from autopublish.platforms.baijiahao import BaijiahaoPublisher
from autopublish.platforms.zhidao import ZhidaoPublisher

BASE_DIR = Path(__file__).resolve().parent.parent
CFG = load_config()

def cmd_list():
    """List pending articles."""
    all_pending = get_pending(CFG["publish_queue_dir"])
    baijia = [p for p in all_pending if p.get("platform") == "baijiahao"]
    zhidao = [p for p in all_pending if p.get("platform") == "zhidao"]
    zhihu = [p for p in all_pending if p.get("platform") == "zhihu"]
    print(f"\n📋 待发布文章 ({len(all_pending)} 篇)")
    print(f"  百家号: {len(baijia)} 篇")
    print(f"  百度知道: {len(zhidao)} 篇")
    print(f"  知乎: {len(zhihu)} 篇")
    for p in all_pending:
        print(f"  [{p.get('platform','?')}] {p.get('title','(无标题)')} → {p.get('_file','')}")
    print()

def cmd_login(platform: str):
    """Start browser and wait for user to log in."""
    print(f"🚀 启动 {platform} 浏览器...")
    engine = BrowserEngine(platform)
    engine.start(headless=False)
    if platform == "baijiahao":
        engine.goto("https://baijiahao.baidu.com/", wait_until="domcontentloaded")
    elif platform == "zhidao":
        engine.goto("https://zhidao.baidu.com/", wait_until="domcontentloaded")
    elif platform == "zhihu":
        engine.goto("https://www.zhihu.com/", wait_until="domcontentloaded")
    else:
        engine.goto("https://www.baidu.com", wait_until="domcontentloaded")
    import time
    time.sleep(2)
    print()
    print("📋 操作步骤:")
    print("   1. 在弹出的浏览器窗口中登录你的账号")
    print("   2. 登录成功后，在终端按 Enter 键确认")
    print()
    input(">>> 登录完成后，请按 Enter 继续...")
    engine.screenshot(str(BASE_DIR / ".workbuddy" / "preview-shots" / f"{platform}_login_check.png"))
    print(f"✅ 已截图验证登录状态")
    print()
    input(">>> 确认没问题后，按 Enter 关闭浏览器...")
    engine.stop()
    print("✅ 登录态已保存")

def cmd_publish(platform: str, index: int = 0):
    """Publish articles from queue."""
    pending = get_pending(CFG["publish_queue_dir"], platform)
    if not pending:
        print(f"📭 没有待发布的 {platform} 文章")
        return

    item = pending[index]
    title = item.get("title", "(无标题)")
    source = item.get("_file", "")
    print(f"📝 准备发布: {title}")
    print(f"   源文件: {source}")

    # Fetch cover image (only baijiahao needs a cover; zhidao/zhihu answers have none)
    cover_path = None
    if platform == "baijiahao":
        keywords = item.get("topic") or title
        try:
            print(f"🖼️  正在为 '{title}' 搜索封面图...")
            cover_path = search_cover(keywords)
            print(f"   封面已下载: {cover_path}")
        except Exception as e:
            print(f"⚠️  封面获取失败: {e}，继续发布（无封面）")

    # Start browser and publish
    engine = BrowserEngine(platform)
    engine.start(headless=False)

    if platform == "baijiahao":
        pub = BaijiahaoPublisher(engine)
    elif platform == "zhidao":
        pub = ZhidaoPublisher(engine)
    else:
        pub = BaijiahaoPublisher(engine)
    result = pub.publish(item, cover_path)

    # Move to published
    if result.get("success"):
        qdir = BASE_DIR / CFG["publish_queue_dir"]
        pdir = BASE_DIR / CFG["published_dir"]
        src = Path(item["_file"])
        dst = pdir / src.name
        if src.exists():
            shutil.move(str(src), str(dst))
        # Update status in the moved file
        content = dst.read_text(encoding="utf-8")
        content = content.replace("status: pending", f'status: published\npublish_time: {str(item.get("_file",""))}')
        dst.write_text(content, encoding="utf-8")
        print(f"✅ 发布成功: {result.get('url', '')}")
    else:
        print(f"❌ 发布失败: {result.get('error', '未知错误')}")

    engine.stop()
    return result

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]
    if cmd == "list":
        cmd_list()
    elif cmd == "login":
        if len(sys.argv) < 3:
            print("用法: autopublish.py login <baijiahao|zhidao|zhihu>")
            return
        cmd_login(sys.argv[2])
    elif cmd == "publish":
        if len(sys.argv) < 3:
            print("用法: autopublish.py publish <baijiahao|zhidao|zhihu> [index]")
            return
        platform = sys.argv[2]
        idx = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        cmd_publish(platform, idx)
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)

if __name__ == "__main__":
    main()
