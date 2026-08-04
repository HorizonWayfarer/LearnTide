# -*- coding: utf-8 -*-
"""给 articles/ 下不走构建器的 legacy 手写页补齐 head 元素。

背景：build_articles.py 的 page_shell() 已统一输出 canonical + OG + twitter 卡片，
但 3 篇 legacy 文章是手写 HTML，不经过构建器，因此这些字段全部缺失。
SEO 审计把 canonical 缺失列为阻断项（社交平台 URL 追参会导致同一页被重复收录）。

本脚本一次性补齐，字段顺序与 page_shell() 保持逐字一致，便于日后比对。
幂等：已有 canonical 的文件会被跳过，可重复运行。
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ARTICLES = os.path.join(HERE, "articles")

SITE_URL = "https://learntide.cc.cd"
SITE_NAME = "Learntide 学习潮汐"
OG_IMAGE = SITE_URL + "/assets/og-default.png"

# 只处理这三篇：其余 10 篇由 build_articles.py 生成，已带全部字段
LEGACY = [
    "ai-chat-assistant-compare",
    "ai-weekly-report-guide",
    "free-ai-image-tools-2026",
]


def pick(html, pattern, default=""):
    m = re.search(pattern, html)
    return m.group(1) if m else default


def fix(slug):
    path = os.path.join(ARTICLES, slug + ".html")
    if not os.path.isfile(path):
        return slug, "文件不存在"

    with open(path, encoding="utf-8") as f:
        html = f.read()

    if 'rel="canonical"' in html:
        return slug, "已有 canonical，跳过"

    canon = "%s/articles/%s.html" % (SITE_URL, slug)
    og_title = pick(html, r'<meta property="og:title" content="([^"]*)"')
    og_desc = pick(html, r'<meta property="og:description" content="([^"]*)"')

    # canonical 紧跟 title，与 page_shell() 顺序一致
    html = html.replace(
        '<link rel="stylesheet"',
        '<link rel="canonical" href="%s">\n<link rel="stylesheet"' % canon,
        1,
    )

    # 社交卡片字段补在 og:type 之后
    extra = "\n".join([
        '<meta property="og:url" content="%s">' % canon,
        '<meta property="og:site_name" content="%s">' % SITE_NAME,
        '<meta property="og:locale" content="zh_CN">',
        '<meta property="og:image" content="%s">' % OG_IMAGE,
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % og_title,
        '<meta name="twitter:description" content="%s">' % og_desc,
        '<meta name="twitter:image" content="%s">' % OG_IMAGE,
        '<meta name="robots" content="index,follow">',
    ])
    m = re.search(r'<meta property="og:type" content="[^"]*">', html)
    if m:
        html = html[: m.end()] + "\n" + extra + html[m.end():]
    else:
        html = html.replace(
            '<link rel="stylesheet"', extra + '\n<link rel="stylesheet"', 1
        )

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    return slug, "已补 canonical + 社交卡片 9 项"


if __name__ == "__main__":
    print("补齐 legacy 手写页 head 元素：")
    for slug in LEGACY:
        name, status = fix(slug)
        print("  %-32s %s" % (name, status))
