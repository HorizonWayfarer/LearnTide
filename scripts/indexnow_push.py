#!/usr/bin/env python3
"""
IndexNow 推送工具 - 向 Bing/Yandex 实时推送 URL 索引

用法：
  python indexnow_push.py init       # 首次配置：生成 key + 验证文件
  python indexnow_push.py push-all   # 推送 sitemap 中全部 URL
  python indexnow_push.py push URL   # 推送单个 URL

配置文件存放在 scripts/indexnow_config.json
"""

import argparse
import json
import os
import secrets
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

# ── 常量 ───────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent  # A:\LearnTide
CONFIG_FILE = SCRIPT_DIR / "indexnow_config.json"
SITEMAP_FILE = PROJECT_ROOT / "sitemap.xml"
SITE_DOMAIN = "learntide.cc.cd"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"

# ── 配置读写 ─────────────────────────────────────────────────────────────
def load_config():
    """加载配置，不存在则返回 None"""
    if not CONFIG_FILE.exists():
        return None
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg):
    """保存配置"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    print(f"[OK] 配置已保存到 {CONFIG_FILE}")


# ── init 命令 ─────────────────────────────────────────────────────────────
def cmd_init():
    """首次配置：生成 API key，创建验证文件，保存配置"""
    print("=== IndexNow 初始化 ===\n")

    # 生成 key（32 位 hex）
    api_key = secrets.token_hex(16)
    print(f"[1/3] 生成 API Key: {api_key}")

    # 在站点根目录创建验证文件
    key_file = PROJECT_ROOT / f"{api_key}.txt"
    with open(key_file, "w", encoding="utf-8") as f:
        f.write(api_key)
    print(f"[2/3] 创建验证文件: {key_file}")
    print(f"      上线后访问 https://{SITE_DOMAIN}/{api_key}.txt 应返回该 key")

    # 保存配置
    cfg = {
        "api_key": api_key,
        "host": SITE_DOMAIN,
        "key_file": str(key_file),
        "key_location": f"https://{SITE_DOMAIN}/{api_key}.txt"
    }
    save_config(cfg)

    print(f"[3/3] 配置完成！\n")
    print("接下来你需要：")
    print(f"  1. 将 {api_key}.txt 部署到网站根目录（git push 或手动上传）")
    print(f"  2. 验证文件可访问：curl https://{SITE_DOMAIN}/{api_key}.txt")
    print(f"  3. 运行: python indexnow_push.py push-all")


# ── URL 提取 ──────────────────────────────────────────────────────────────
def extract_urls_from_sitemap():
    """从 sitemap.xml 提取所有 <loc> URL"""
    if not SITEMAP_FILE.exists():
        print(f"[ERROR] 找不到 sitemap.xml: {SITEMAP_FILE}")
        sys.exit(1)

    import re
    text = SITEMAP_FILE.read_text(encoding="utf-8")
    urls = re.findall(r"<loc>(.*?)</loc>", text)
    print(f"[INFO] 从 sitemap.xml 提取到 {len(urls)} 个 URL")
    return urls


# ── 推送逻辑 ──────────────────────────────────────────────────────────────
def push_urls(urls, cfg):
    """
    向 IndexNow API 推送 URL 列表
    
    返回 (success_count, error_list)
    """
    api_key = cfg["api_key"]
    host = cfg["host"]
    key_location = cfg["key_location"]

    # 分批推送（每批最多 10000 个，官方限制）
    BATCH_SIZE = 10000
    success = 0
    errors = []

    for i in range(0, len(urls), BATCH_SIZE):
        batch = urls[i : i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        total_batches = (len(urls) + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"\n[推送] 第 {batch_num}/{total_batches} 批，共 {len(batch)} 个 URL")

        payload = {
            "host": host,
            "key": api_key,
            "keyLocation": key_location,
            "urlList": batch
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            INDEXNOW_ENDPOINT,
            data=data,
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                status = resp.getcode()
                print(f"  HTTP {status}: {'URL 已接收' if status in (200, 202) else resp.read().decode()}")
                if status in (200, 202):
                    success += len(batch)
                else:
                    errors.append({"batch": batch_num, "status": status})
        except urllib.error.HTTPError as e:
            body = e.read().decode() if e.fp else ""
            print(f"  [ERROR] HTTP {e.code}: {body}")
            errors.append({"batch": batch_num, "status": e.code, "body": body})
        except urllib.error.URLError as e:
            print(f"  [ERROR] 网络错误: {e.reason}")
            errors.append({"batch": batch_num, "error": str(e.reason)})

        # 礼貌延迟：避免 429 Too Many Requests
        if i + BATCH_SIZE < len(urls):
            print("  等待 2 秒...")
            time.sleep(2)

    return success, errors


def cmd_push_all():
    """推送 sitemap 中全部 URL"""
    print("=== IndexNow 全量推送 ===\n")

    cfg = load_config()
    if not cfg:
        print("[ERROR] 未找到配置，请先运行: python indexnow_push.py init")
        sys.exit(1)

    urls = extract_urls_from_sitemap()
    if not urls:
        print("[WARN] sitemap.xml 为空，无需推送")
        return

    print(f"\n[INFO] API Key: {cfg['api_key'][:8]}...{cfg['api_key'][-4:]}")
    print(f"[INFO] Host: {cfg['host']}")
    print(f"[INFO] Endpoint: {INDEXNOW_ENDPOINT}")

    success, errors = push_urls(urls, cfg)

    print(f"\n=== 完成 ===")
    print(f"成功: {success} / {len(urls)}")
    if errors:
        print(f"失败批次: {len(errors)}")
        for err in errors:
            print(f"  {err}")


def cmd_push_url(url):
    """推送单个 URL"""
    print("=== IndexNow 单条推送 ===\n")

    cfg = load_config()
    if not cfg:
        print("[ERROR] 未找到配置，请先运行: python indexnow_push.py init")
        sys.exit(1)

    # 校验 URL 是否属于本站
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc != cfg["host"]:
        print(f"[ERROR] URL 不属于本站 ({cfg['host']}): {url}")
        print("       如需推送其他域名，请修改配置或为该域名单独 init")
        sys.exit(1)

    print(f"[INFO] 推送 URL: {url}")
    print(f"[INFO] API Key: {cfg['api_key'][:8]}...{cfg['api_key'][-4:]}")

    success, errors = push_urls([url], cfg)

    if success:
        print(f"\n[OK] 推送成功，Bing 将在数分钟内抓取")
    else:
        print(f"\n[ERROR] 推送失败: {errors}")


# ── 入口 ──────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="IndexNow 推送工具 - 向 Bing/Yandex 实时推送 URL"
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # init
    subparsers.add_parser("init", help="首次配置：生成 key + 验证文件")

    # push-all
    subparsers.add_parser("push-all", help="推送 sitemap 中全部 URL")

    # push
    push_parser = subparsers.add_parser("push", help="推送单个 URL")
    push_parser.add_argument("url", help="要推送的完整 URL")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command == "push-all":
        cmd_push_all()
    elif args.command == "push":
        cmd_push_url(args.url)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
