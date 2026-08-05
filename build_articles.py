#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Learntide 文章构建器
============================================================================
把 drafts/*.md（YAML front-matter + Markdown 正文）编译成 articles/*.html，
并自动重建：articles.html 归档页、index.html 最新文章列表、sitemap.xml。

设计原则
  - 生成的 HTML 完全复用 assets/style.css 里的既有 class，不引入新框架
  - 每页自带 title / meta description / Open Graph / JSON-LD Article
  - 目录（.toc）由正文 H2 自动生成，锚点为 sec-1、sec-2 …
  - 内链走 front-matter 的 internal_links，渲染为文末「相关阅读」区块

用法
    python build_articles.py                 # 全量构建
    python build_articles.py --dry-run       # 只校验不写文件
    python build_articles.py --only a,b      # 只编译指定 slug（索引仍全量重建）
============================================================================
"""

import argparse
import html
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
DRAFTS_DIR = os.path.join(ROOT, "drafts")
ARTICLES_DIR = os.path.join(ROOT, "articles")
SITE_URL = "https://learntide.cc.cd"
SITE_NAME = "Learntide 学习潮汐"
OG_IMAGE = SITE_URL + "/assets/og-default.png"  # 1200×630 站点默认分享图

# 栏目 → 首页/归档页展示顺序
CATEGORY_ORDER = ["工具测评", "使用教程", "资讯科普"]

# 字数按文章类型分档（front-matter 的 article_type 字段，缺省按 compare）。
# 依据：对比型信息密度高，750-850 够用；清单型受并列款数挤压，每款要留
# 出「适合谁/免费边界/什么情况别用」的空间，故放宽到 950-1100。
WORD_RANGES = {
    "compare": (750, 850),    # 2-5 款深度对比
    "tutorial": (800, 900),   # 步骤流程类
    "list": (950, 1100),      # ≥6 款并列推荐
    "explainer": (800, 900),  # 概念解释类
}
# 兼容 brief 里可能出现的别名写法
CATEGORY_ALIAS = {
    "AI工具": "工具测评", "工具": "工具测评", "AI 工具": "工具测评",
    "教程": "使用教程", "AI教程": "使用教程", "AI 教程": "使用教程",
    "资讯": "资讯科普", "科普": "资讯科普", "AI资讯": "资讯科普",
}

# 早期手写的文章：不走 drafts 流水线，但要进归档页和 sitemap
LEGACY_ARTICLES = [
    {
        "slug": "ai-weekly-report-guide",
        "title": "用 AI 写周报：从流水账到一眼看懂",
        "category": "使用教程",
        "date": "2026-08-04",
        "summary": "把一周的散碎工作交给 AI 整理成结构化周报，附可直接复用的提示词模板。",
    },
    {
        "slug": "free-ai-image-tools-2026",
        "title": "2026 免费 AI 做图工具横评",
        "category": "工具测评",
        "date": "2026-08-04",
        "summary": "即梦、可灵、通义万相、醒图，按需求对号入座，不盲选。",
    },
    {
        "slug": "ai-chat-assistant-compare",
        "title": "AI 对话助手怎么选",
        "category": "工具测评",
        "date": "2026-08-04",
        "summary": "ChatGPT、Claude、Kimi、通义千问，按场景定位对比，不排座次。",
    },
]

CJK_RE = re.compile(r"[\u4e00-\u9fff]")


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def esc(s):
    """HTML 转义（& < > "）。"""
    return html.escape(s, quote=True)


def cjk_count(text):
    """统计中文字数——字数达标校验用。"""
    return len(CJK_RE.findall(text))


def strip_quotes(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def smart_join(lines):
    """
    拼接段落内的多行。中文之间直接相连（不补空格），
    英文/数字边界处补一个空格，避免 "AI工具the best" 这类粘连。
    """
    if not lines:
        return ""
    out = lines[0]
    for nxt in lines[1:]:
        if not nxt:
            continue
        left = out[-1] if out else ""
        right = nxt[0]
        if CJK_RE.match(left) or CJK_RE.match(right):
            out += nxt
        else:
            out += " " + nxt
    return out


# ---------------------------------------------------------------------------
# front-matter 解析（只支持本项目用到的子集：标量 + 对象数组）
# ---------------------------------------------------------------------------

def parse_front_matter(text, source):
    if not text.lstrip().startswith("---"):
        raise ValueError("%s：缺少 YAML front-matter" % source)
    text = text.lstrip()
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("%s：front-matter 未闭合" % source)
    raw = text[3:end].strip("\n")
    body = text[end + 4:].lstrip("\n")

    data = {}
    cur_list = None
    cur_item = None
    for line in raw.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        s = line.strip()
        if indent == 0:
            key, _, val = s.partition(":")
            key, val = key.strip(), val.strip()
            if val == "":
                cur_list = []
                data[key] = cur_list
                cur_item = None
            else:
                data[key] = strip_quotes(val)
                cur_list = None
                cur_item = None
        else:
            if cur_list is None:
                continue
            if s.startswith("- "):
                cur_item = {}
                cur_list.append(cur_item)
                s = s[2:].strip()
                if s:
                    k, _, v = s.partition(":")
                    cur_item[k.strip()] = strip_quotes(v)
            elif cur_item is not None:
                k, _, v = s.partition(":")
                cur_item[k.strip()] = strip_quotes(v)
    return data, body


# ---------------------------------------------------------------------------
# Markdown → HTML（行状态机，只覆盖本项目约定的语法子集）
# ---------------------------------------------------------------------------

def inline(s):
    """行内标记：`code`、**strong**、[text](url)。"""
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)

    def _a(m):
        text, url = m.group(1), m.group(2)
        if url.startswith(("http://", "https://")):   # 外链新窗口 + 防 opener 劫持
            return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, text)
        return '<a href="%s">%s</a>' % (url, text)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", _a, s)
    return s


def split_row(line):
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def is_block_start(s):
    return (
        s.startswith("```")
        or s.startswith("#")
        or s.startswith("|")
        or s.startswith("> ")
        or re.match(r"^[-*]\s+", s) is not None
        or re.match(r"^\d+\.\s+", s) is not None
    )


def md_to_html(body):
    """返回 (html 字符串, [(锚点 id, H2 标题)])。"""
    lines = body.split("\n")
    out, sections = [], []
    i, n = 0, len(lines)

    while i < n:
        s = lines[i].strip()

        # 空行
        if not s:
            i += 1
            continue

        # 围栏代码块
        if s.startswith("```"):
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % esc("\n".join(buf)))
            continue

        # 标题
        m = re.match(r"^(#{2,4})\s+(.*)$", s)
        if m:
            level, title = len(m.group(1)), m.group(2).strip()
            if level == 2:
                sid = "sec-%d" % (len(sections) + 1)
                sections.append((sid, title))
                out.append('<h2 id="%s">%s</h2>' % (sid, inline(title)))
            else:
                out.append("<h%d>%s</h%d>" % (level, inline(title), level))
            i += 1
            continue

        # 表格
        if s.startswith("|") and i + 1 < n and re.match(r"^\|[\s:\-|]+\|$", lines[i + 1].strip()):
            header = split_row(s)
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i].strip()))
                i += 1
            thead = "".join("<th>%s</th>" % inline(c) for c in header)
            tbody = "".join(
                "<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r) for r in rows
            )
            out.append(
                '<div class="table-wrap"><table>'
                "<thead><tr>%s</tr></thead><tbody>%s</tbody>"
                "</table></div>" % (thead, tbody)
            )
            continue

        # 引用块
        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote>%s</blockquote>" % inline(smart_join(buf)))
            continue

        # 无序 / 有序列表
        for pattern, tag in ((r"^[-*]\s+(.*)$", "ul"), (r"^\d+\.\s+(.*)$", "ol")):
            if re.match(pattern, s):
                items = []
                while i < n:
                    mm = re.match(pattern, lines[i].strip())
                    if not mm:
                        break
                    items.append(mm.group(1).strip())
                    i += 1
                out.append(
                    "<%s>%s</%s>"
                    % (tag, "".join("<li>%s</li>" % inline(x) for x in items), tag)
                )
                break
        else:
            # 段落
            buf = []
            while i < n and lines[i].strip() and not is_block_start(lines[i].strip()):
                buf.append(lines[i].strip())
                i += 1
            out.append("<p>%s</p>" % inline(smart_join(buf)))
            continue
        continue

    return "\n\n".join(out), sections


# ---------------------------------------------------------------------------
# 页面模板
# ---------------------------------------------------------------------------

def nav_html(prefix, active):
    """prefix: 根页面为 ''，articles/ 下为 '../'。"""
    items = [
        ("home", "首页", prefix + "index.html"),
        ("tools", "AI 工具", prefix + "tools.html"),
        ("articles", "全部文章", prefix + "articles.html"),
        ("about", "关于", prefix + "about.html"),
    ]
    parts = []
    for key, label, href in items:
        if key == active:
            parts.append(
                '      <a href="%s" class="active" aria-current="page">%s</a>' % (href, label)
            )
        else:
            parts.append('      <a href="%s">%s</a>' % (href, label))
    return "\n".join(parts)


def page_shell(prefix, active, title, description, head_extra, body,
               og_type="website", canonical=""):
    """canonical 必须传绝对 URL，且与 sitemap.xml 中的写法逐字一致。"""
    canon = canonical or SITE_URL + "/"
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="canonical" href="{canon}">
<link rel="stylesheet" href="{prefix}assets/style.css">
<link rel="icon" type="image/svg+xml" href="{prefix}assets/learntide-logo.svg">
<meta name="description" content="{desc}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="{site_name}">
<meta property="og:locale" content="zh_CN">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<meta name="robots" content="index,follow">
{head_extra}</head>
<body>
<header class="site-header">
  <div class="container">
    <span class="brand"><img class="brand-logo" src="{prefix}assets/learntide-logo.svg" alt="Learntide 学习潮汐" width="28" height="28"><span class="brand-name">Learn<b>Tide</b></span><small>学习潮汐</small></span>
    <nav class="nav">
{nav}
    </nav>
  </div>
</header>

{body}

<footer class="site-footer">
  <div class="container">
    Learntide · 学习潮汐 — 内容站（信息流动）。© 2026 · <a href="{prefix}about.html">关于本站</a>
  </div>
</footer>
</body>
</html>
""".format(
        title=esc(title),
        prefix=prefix,
        canon=esc(canon),
        desc=esc(description),
        og_title=esc(title.split(" — ")[0]),
        og_type=og_type,
        og_image=OG_IMAGE,
        site_name=esc(SITE_NAME),
        head_extra=head_extra,
        nav=nav_html(prefix, active),
        body=body,
    )


def render_article(meta, body_html, sections, slug_index):
    slug = meta["slug"]
    title = meta["title"]
    category = meta["category"]
    pub = meta.get("date", str(date.today()))

    # 目录：H2 少于 3 个就不渲染，避免小文章顶一坨空目录
    toc = ""
    if len(sections) >= 3:
        lis = "\n".join(
            '      <li><a href="#%s">%s</a></li>' % (sid, esc(t)) for sid, t in sections
        )
        toc = """  <div class="toc">
    <h4><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 4h8M6 8h8M6 12h8"/><path d="M3 4h.01M3 8h.01M3 12h.01"/></svg>本文目录</h4>
    <ol>
%s
    </ol>
  </div>

""" % lis

    # 相关阅读
    related = ""
    links = meta.get("internal_links") or []
    if links:
        lis = []
        for ln in links:
            anchor = ln.get("anchor", "")
            if ln.get("slug"):
                target = ln["slug"]
                # 目标文章尚未产出时跳过，避免死链
                if target not in slug_index:
                    continue
                href = target + ".html"
                if not anchor:
                    anchor = slug_index[target]
            elif ln.get("path"):
                href = ln["path"]
            else:
                continue
            lis.append('      <li><a href="%s">%s</a></li>' % (esc(href), esc(anchor)))
        if lis:
            related = """
  <aside class="related">
    <h4>相关阅读</h4>
    <ul>
%s
    </ul>
  </aside>
""" % "\n".join(lis)

    verified = meta.get("verified", "")
    verify_note = ""
    if verified:
        verify_note = (
            '\n  <p class="verify-note">本文信息核对于 %s。AI 产品的价格、'
            "免费额度与功能变动频繁，实际以各工具官网当前说明为准。</p>\n" % esc(verified)
        )

    canon = "%s/articles/%s.html" % (SITE_URL, slug)
    mod = meta.get("verified") or pub  # dateModified 反映真实修订日期

    ld = """<script type="application/ld+json">
{{
  "@context":"https://schema.org","@type":"Article",
  "headline":"{h}",
  "description":"{d}",
  "image":"{img}",
  "datePublished":"{p}","dateModified":"{m}",
  "inLanguage":"zh-CN",
  "articleSection":"{cat}",
  "mainEntityOfPage":{{"@type":"WebPage","@id":"{canon}"}},
  "author":{{"@type":"Organization","name":"{n}"}},
  "publisher":{{"@type":"Organization","name":"{n}"}}
}}
</script>
<script type="application/ld+json">
{{
  "@context":"https://schema.org","@type":"BreadcrumbList",
  "itemListElement":[
    {{"@type":"ListItem","position":1,"name":"首页","item":"{u}/"}},
    {{"@type":"ListItem","position":2,"name":"{cat}","item":"{u}/articles.html"}},
    {{"@type":"ListItem","position":3,"name":"{h}"}}
  ]
}}
</script>
""".format(
        h=esc(title),
        d=esc(meta.get("meta_description", "")),
        img=OG_IMAGE,
        p=pub,
        m=mod,
        cat=esc(category),
        u=SITE_URL,
        canon=canon,
        n=SITE_NAME,
    )

    # 可见面包屑：Google 要求结构化数据与页面可见内容一致
    crumb = """  <nav class="breadcrumb" aria-label="面包屑">
    <a href="../index.html">首页</a>
    <span aria-hidden="true">›</span>
    <a href="../articles.html">{cat}</a>
    <span aria-hidden="true">›</span>
    <span class="current">{h1}</span>
  </nav>
""".format(cat=esc(category), h1=esc(title))

    body = """<article class="article">
{crumb}  <h1>{h1}</h1>
  <div class="article-meta">{cat} · {pub}</div>
  <p class="lede">{lede}</p>

{toc}{content}
{verify}{related}</article>""".format(
        crumb=crumb,
        h1=esc(title),
        cat=esc(category),
        pub=esc(pub),
        lede=inline(meta.get("lede", "")),
        toc=toc,
        content=body_html,
        verify=verify_note,
        related=related,
    )

    return page_shell(
        prefix="../",
        active="articles",
        title=meta.get("meta_title") or (title + " — Learntide"),
        description=meta.get("meta_description", ""),
        head_extra=ld,
        body=body,
        og_type="article",
        canonical=canon,
    )


def render_archive(posts):
    """全部文章归档页：按栏目分组，随文章增长自然扩容。"""
    groups = {c: [] for c in CATEGORY_ORDER}
    for p in posts:
        groups.setdefault(p["category"], []).append(p)

    blocks = []
    for cat in CATEGORY_ORDER:
        items = groups.get(cat) or []
        if not items:
            continue
        items.sort(key=lambda x: (x["date"], x["title"]), reverse=True)
        cards = "\n".join(
            """      <a class="card" href="articles/{s}.html">
        <h3>{t}</h3>
        <div class="meta">{c} · {d}</div>
        <p>{p}</p>
      </a>""".format(
                s=esc(x["slug"]),
                t=esc(x["title"]),
                c=esc(x["category"]),
                d=esc(x["date"]),
                p=esc(x["summary"]),
            )
            for x in items
        )
        blocks.append(
            """<section class="section">
  <div class="container">
    <h2>{cat}<span class="count">{n} 篇</span></h2>
    <div class="card-grid">
{cards}
    </div>
  </div>
</section>""".format(cat=esc(cat), n=len(items), cards=cards)
        )

    body = """<section class="hero">
  <div class="container">
    <h1>全部文章</h1>
    <p>共 {total} 篇，按栏目归档。工具测评讲清免费额度与国内可用性，教程给可直接复制的提示词，科普用大白话。</p>
  </div>
</section>

{blocks}""".format(total=len(posts), blocks="\n\n".join(blocks))

    canon = SITE_URL + "/articles.html"
    ld = """<script type="application/ld+json">
{{
  "@context":"https://schema.org","@type":"CollectionPage",
  "name":"全部文章",
  "description":"Learntide 全部 AI 文章归档，按栏目分类。",
  "url":"{canon}",
  "inLanguage":"zh-CN",
  "isPartOf":{{"@type":"WebSite","name":"{n}","url":"{u}/"}}
}}
</script>
<script type="application/ld+json">
{{
  "@context":"https://schema.org","@type":"BreadcrumbList",
  "itemListElement":[
    {{"@type":"ListItem","position":1,"name":"首页","item":"{u}/"}},
    {{"@type":"ListItem","position":2,"name":"全部文章"}}
  ]
}}
</script>
""".format(canon=canon, u=SITE_URL, n=esc(SITE_NAME))

    return page_shell(
        prefix="",
        active="articles",
        title="全部文章 — Learntide 学习潮汐",
        description="Learntide 全部 AI 文章归档：AI 工具测评、AI 使用教程、AI 资讯科普，按栏目分类浏览，持续更新。",
        head_extra=ld,
        body=body,
        canonical=canon,
    )


# ---------------------------------------------------------------------------
# 索引重建：index.html / sitemap.xml
# ---------------------------------------------------------------------------

HOME_START = "<!-- ARTICLES:START -->"
HOME_END = "<!-- ARTICLES:END -->"


def update_homepage(posts, dry_run=False):
    path = os.path.join(ROOT, "index.html")
    with open(path, encoding="utf-8") as f:
        src = f.read()
    if HOME_START not in src or HOME_END not in src:
        print("  ! index.html 缺少 ARTICLES:START/END 标记，跳过首页更新")
        return
    latest = sorted(posts, key=lambda x: (x["date"], x["slug"]), reverse=True)[:6]
    cards = "\n".join(
        """      <a class="card" href="articles/{s}.html">
        <h3>{t}</h3>
        <div class="meta">{c} · {d}</div>
        <p>{p}</p>
      </a>""".format(
            s=esc(x["slug"]), t=esc(x["title"]), c=esc(x["category"]),
            d=esc(x["date"]), p=esc(x["summary"]),
        )
        for x in latest
    )
    block = "%s\n%s\n    %s" % (HOME_START, cards, HOME_END)
    new = re.sub(
        re.escape(HOME_START) + r".*?" + re.escape(HOME_END), block, src, flags=re.S
    )
    if not dry_run:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new)
    print("  · index.html 最新文章已刷新（%d 张卡片）" % len(latest))


def update_sitemap(posts, dry_run=False):
    path = os.path.join(ROOT, "sitemap.xml")
    today = str(date.today())
    rows = [
        '  <url><loc>%s/</loc><lastmod>%s</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>' % (SITE_URL, today),
        '  <url><loc>%s/articles.html</loc><lastmod>%s</lastmod><changefreq>daily</changefreq><priority>0.9</priority></url>' % (SITE_URL, today),
        '  <url><loc>%s/tools.html</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>' % (SITE_URL, today),
        '  <url><loc>%s/about.html</loc><changefreq>monthly</changefreq><priority>0.4</priority></url>' % SITE_URL,
    ]
    for p in sorted(posts, key=lambda x: x["slug"]):
        rows.append(
            '  <url><loc>%s/articles/%s.html</loc><lastmod>%s</lastmod>'
            "<changefreq>monthly</changefreq><priority>0.7</priority></url>"
            % (SITE_URL, p["slug"], p["date"])
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )
    if not dry_run:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(xml)
    print("  · sitemap.xml 已重建（%d 条 URL）" % len(rows))


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = ["slug", "title", "category", "meta_title", "meta_description", "lede"]


def main():
    ap = argparse.ArgumentParser(description="Learntide 文章构建器")
    ap.add_argument("--dry-run", action="store_true", help="只校验、不写文件")
    ap.add_argument("--only", default="", help="只编译指定 slug，逗号分隔")
    args = ap.parse_args()

    only = {s.strip() for s in args.only.split(",") if s.strip()}

    if not os.path.isdir(DRAFTS_DIR):
        print("找不到 drafts/ 目录：%s" % DRAFTS_DIR)
        return 1
    os.makedirs(ARTICLES_DIR, exist_ok=True)

    files = sorted(
        os.path.join(DRAFTS_DIR, f) for f in os.listdir(DRAFTS_DIR) if f.endswith(".md")
    )
    if not files:
        print("drafts/ 下没有 .md 文件")
        return 1

    parsed, errors = [], []
    for fp in files:
        name = os.path.basename(fp)
        try:
            with open(fp, encoding="utf-8") as f:
                meta, body = parse_front_matter(f.read(), name)
        except ValueError as e:
            errors.append(str(e))
            continue
        meta["category"] = CATEGORY_ALIAS.get(meta.get("category", ""), meta.get("category", ""))
        missing = [k for k in REQUIRED_FIELDS if not meta.get(k)]
        if missing:
            errors.append("%s：front-matter 缺字段 %s" % (name, ", ".join(missing)))
            continue
        if meta["category"] not in CATEGORY_ORDER:
            errors.append("%s：category「%s」不在 %s 内" % (name, meta["category"], CATEGORY_ORDER))
            continue
        meta.setdefault("date", str(date.today()))
        parsed.append((meta, body))

    if errors:
        print("front-matter 校验未通过：")
        for e in errors:
            print("  ! " + e)
        return 1

    # slug 索引（含 legacy），供内链存在性校验
    slug_index = {m["slug"]: m["title"] for m, _ in parsed}
    for lg in LEGACY_ARTICLES:
        slug_index.setdefault(lg["slug"], lg["title"])

    posts = list(LEGACY_ARTICLES)
    inbound = {s: 0 for s in slug_index}          # 内链体检：每个 slug 收到的入链数
    outbound = {}                                 # 每篇发出的站内文章链接数
    print("编译 %d 篇：" % len(parsed))
    for meta, body in parsed:
        slug = meta["slug"]
        body_html, sections = md_to_html(body)
        words = cjk_count(re.sub(r"```.*?```", "", body, flags=re.S))
        atype = (meta.get("article_type") or "compare").strip()
        lo, hi = WORD_RANGES.get(atype, WORD_RANGES["compare"])
        flag = "" if lo <= words <= hi else "  ← 字数偏离 %s 档 %d–%d" % (atype, lo, hi)
        print("  · %-32s %4d 字  H2×%d  [%s]%s"
              % (slug, words, len(sections), atype, flag))

        if not only or slug in only:
            page = render_article(meta, body_html, sections, slug_index)
            if not args.dry_run:
                with open(
                    os.path.join(ARTICLES_DIR, slug + ".html"), "w",
                    encoding="utf-8", newline="\n",
                ) as f:
                    f.write(page)

        # 内链体检：front-matter 内链 + 正文手写内链，都算一条入链
        outs = 0
        for lk in meta.get("internal_links") or []:
            tgt = (lk.get("slug") or "").strip()
            if not tgt and lk.get("path", "").endswith(".html"):
                tgt = os.path.basename(lk["path"])[:-5]
            if tgt in inbound:
                inbound[tgt] += 1
                outs += 1
        for _a, href in re.findall(r"\[([^\]]+)\]\(([^)\s]+)\)", body):
            tgt = os.path.basename(href.split("#")[0])
            if tgt.endswith(".html") and tgt[:-5] in inbound:
                inbound[tgt[:-5]] += 1
                outs += 1
        outbound[slug] = outs

        posts.append({
            "slug": slug,
            "title": meta["title"],
            "category": meta["category"],
            "date": meta["date"],
            "summary": meta.get("lede") or meta.get("meta_description", ""),
        })

    orphans = sorted(s for s, n in inbound.items() if n == 0)
    deadends = sorted(s for s, n in outbound.items() if n == 0)
    if orphans or deadends:
        print("\n内链体检：")
        if orphans:
            print("  ! 孤岛（0 条站内入链）：%s" % "、".join(orphans))
        if deadends:
            print("  ! 死胡同（0 条站内出链）：%s" % "、".join(deadends))
    else:
        print("\n内链体检：无孤岛、无死胡同。")

    print("重建索引：")
    if not args.dry_run:
        with open(os.path.join(ROOT, "articles.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(render_archive(posts))
    print("  · articles.html 归档页已重建（%d 篇）" % len(posts))
    update_homepage(posts, args.dry_run)
    update_sitemap(posts, args.dry_run)

    print("\n完成。%s" % ("（dry-run，未写入任何文件）" if args.dry_run else "共 %d 篇上线内容。" % len(posts)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
