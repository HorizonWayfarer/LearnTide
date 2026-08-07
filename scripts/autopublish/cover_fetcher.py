"""Fetch cover images from Pexels API."""
import os
import time
import json
import requests
from pathlib import Path
from urllib.parse import quote

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = Path(__file__).resolve().parent / "config.json"

def _load_key():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg["pexels_api_key"]

TARGET_RATIO = 3 / 2  # 目标封面宽高比 3:2 (=1.5)
MIN_RATIO = 1.25       # 低于此比例视为太方/竖图，直接排除

def _pexels_search(kw: str, api_key: str) -> list:
    """Search Pexels, returns list of photo objects (landscape only)."""
    # orientation=landscape 让 Pexels 端只返回横图
    url = (
        f"https://api.pexels.com/v1/search?query={quote(kw)}"
        f"&orientation=landscape&size=large&per_page=15"
    )
    headers = {"Authorization": api_key}
    resp = requests.get(url, headers=headers, timeout=30, proxies={"http": None, "https": None})
    resp.raise_for_status()
    return resp.json().get("photos", [])

def _rank_by_ratio(photos: list) -> list:
    """按『最接近 3:2 横图』给候选排序，并排除竖图/方图。"""
    scored = []
    for p in photos:
        w, h = p.get("width", 0), p.get("height", 0)
        if not w or not h:
            continue
        ratio = w / h
        if ratio < MIN_RATIO:      # 竖图或接近正方形，跳过
            continue
        scored.append((abs(ratio - TARGET_RATIO), p))
    scored.sort(key=lambda x: x[0])   # 差值越小越接近 3:2，排越前
    return [p for _, p in scored]

def search_cover(keywords: str) -> str:
    """
    Search Pexels for a cover image.
    Returns the local path of downloaded image.
    Retries with multiple keyword variants.
    """
    api_key = _load_key()
    candidates = [
        keywords,
        keywords.replace("测评", "review").replace("横评", "comparison"),
        keywords.replace("教程", "tutorial"),
        keywords.replace("AI", "artificial intelligence"),
        "artificial intelligence tools",
        "technology tools",
        "creative workspace",
    ]
    seen_urls = set()

    for kw in candidates:
        try:
            photos = _rank_by_ratio(_pexels_search(kw, api_key))
            for photo in photos:
                # large2x 保持原始比例（我们已按原始 w/h 挑了接近 3:2 的图）；
                # 不用 src.landscape，那是裁成 1.91:1 的，反而偏宽。
                img = (
                    photo.get("src", {}).get("large2x")
                    or photo.get("src", {}).get("large")
                    or photo.get("src", {}).get("original")
                )
                if not img or img in seen_urls:
                    continue
                seen_urls.add(img)
                w, h = photo.get("width", 0), photo.get("height", 0)
                ratio = round(w / h, 2) if h else "?"
                cover_dir = BASE_DIR / "assets" / "covers"
                cover_dir.mkdir(parents=True, exist_ok=True)
                safe_kw = "".join(c for c in kw[:20] if c.isalnum())
                fname = f"{safe_kw}_{photo['id']}.jpg"
                fpath = cover_dir / fname
                r2 = requests.get(img, timeout=60, proxies={"http": None, "https": None})
                r2.raise_for_status()
                fpath.write_bytes(r2.content)
                print(f"[cover] Downloaded via '{kw}' (ratio {ratio}): {fpath}")
                return str(fpath)
        except Exception as e:
            print(f"[cover] Keyword '{kw}' failed: {e}")
            continue

    raise RuntimeError(f"No cover image found after trying all keyword variants for: {keywords}")
