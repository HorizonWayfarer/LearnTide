#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为每篇文章从 Pexels 拉取独立封面图，存 assets/covers/{slug}.jpg。

策略
  - 按分类批量搜索（每类一次请求，per_page=80），降低 API 调用量
  - 组内文章按日期排序后轮询分配候选图，保证同类文章不撞图
  - 已存在的图跳过，可安全重复运行（不重复消耗额度）

依赖：本地 scripts/autopublish/config.json 中的 pexels_api_key（该文件已被 gitignore）。
"""
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CFG = json.loads((ROOT / "scripts/autopublish/config.json").read_text(encoding="utf-8"))
KEY = CFG["pexels_api_key"]
COVERS = ROOT / "assets" / "covers"
COVERS.mkdir(parents=True, exist_ok=True)

# 走本地代理（FlClash，端口 7890），否则 urllib 直连会被防火墙拒绝
_raw = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or "http://127.0.0.1:7890"
_PROXY = _raw.rstrip("/")  # 规范化：去掉末尾斜杠，避免 urllib 解析异常
_opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": _PROXY, "https": _PROXY})
)

# 分类 -> Pexels 英文搜索词（保证科技/AI 调性，与站点主题一致）
QUERY = {
    "工具测评": "AI software application interface",
    "使用教程": "laptop workspace productivity",
    "资讯科普": "artificial intelligence technology",
}


def parse_min(path):
    """最小 front-matter 解析：只取 slug / category / date。"""
    text = Path(path).read_text(encoding="utf-8")
    if not text.lstrip().startswith("---"):
        return None
    text = text.lstrip()
    end = text.find("\n---", 3)
    if end == -1:
        return None
    raw = text[3:end].strip("\n")
    d = {}
    for line in raw.split("\n"):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        k, _, v = s.partition(":")
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k in ("slug", "category", "date"):
            d[k] = v
    return d


def fetch(query, per_page=80):
    url = "https://api.pexels.com/v1/search?query=%s&per_page=%d" % (
        urllib.parse.quote(query),
        per_page,
    )
    req = urllib.request.Request(url, headers={"Authorization": KEY, "User-Agent": "Mozilla/5.0"})
    with _opener.open(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8")).get("photos", [])


def dl(photo, dest):
    # medium 尺寸（~780px）加载更快更稳，卡片 16:9 展示完全足够；
    # large 原图太大，慢网络下 30s 超时导致失败回退到分类默认图
    src = photo["src"]["medium"]
    req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
    with _opener.open(req, timeout=60) as r:
        dest.write_bytes(r.read())


def main():
    drafts = sorted(ROOT.glob("drafts/*.md"))
    groups = {}
    for p in drafts:
        d = parse_min(p)
        if not d or "slug" not in d or "category" not in d:
            continue
        groups.setdefault(d["category"], []).append(d)

    total = 0
    for cat, items in groups.items():
        items.sort(key=lambda x: x.get("date", ""), reverse=True)
        photos = fetch(QUERY.get(cat, "artificial intelligence"))
        print("[%s] %d 篇, 候选图 %d 张" % (cat, len(items), len(photos)))
        for i, d in enumerate(items):
            slug = d["slug"]
            dest = COVERS / ("%s.jpg" % slug)
            if dest.exists():
                continue
            if not photos:
                print("  ! 无候选图, 跳过 %s" % slug)
                break
            ph = photos[i % len(photos)]
            for attempt in range(3):
                try:
                    dl(ph, dest)
                    total += 1
                    print("  + %s <- %s" % (slug, ph["url"]))
                    time.sleep(0.3)
                    break
                except Exception as e:
                    print("  ! %s 第%d次失败: %s" % (slug, attempt + 1, e))
                    time.sleep(1)
            else:
                print("  ! %s 三次重试仍失败, 跳过" % slug)
    print("完成, 新增 %d 张封面" % total)


if __name__ == "__main__":
    main()
