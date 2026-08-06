#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除文章前，批量清理所有指向待删 slug 的内链引用。
- front matter 的 internal_links 条目（path/slug + anchor）
- 正文里的 markdown 链接 [text](slug.html)
避免留下死链（404）。

用法：
    python scripts/clean_orphan_refs.py --dry-run
    python scripts/clean_orphan_refs.py --apply
"""
import os
import re
import sys

DRAFTS_DIR = os.path.join(os.path.dirname(__file__), "..", "drafts")
TARGETS = [
    "ai-chat-assistant-compare",
    "ai-weekly-report-guide",
    "free-ai-image-tools-2026",
]

# FM 内链条目：  - path: TARGET.html  /  - slug: TARGET  （含可选 anchor 行）
FM_ENTRY = re.compile(
    r"^[ \t]*-[ \t]+(?:path|slug):[ \t]*("
    + "|".join(re.escape(t) for t in TARGETS)
    + r")(?:\.html)?[ \t]*\n(?:[ \t]+anchor:[^\n]*\n)?",
    re.MULTILINE,
)

# 正文 markdown 链接 [text](TARGET.html)
BODY_LINK = re.compile(
    r"\[([^\]]+)\]\("
    + r"("
    + "|".join(re.escape(t) for t in TARGETS)
    + r")\.html\)"
)


def clean_text(text):
    """返回 (new_text, fm_changed, body_changed)。"""
    # 分离 front matter
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if m:
        fm, body = m.group(1), m.group(2)
    else:
        fm, body = "", text

    new_fm = FM_ENTRY.sub("", fm)
    fm_changed = new_fm != fm

    new_body = BODY_LINK.sub(r"\1", body)
    body_changed = new_body != body

    if m:
        new_text = "---\n" + new_fm + "\n---\n" + new_body
    else:
        new_text = new_body

    return new_text, fm_changed, body_changed


def main():
    apply = "--apply" in sys.argv
    total = 0
    for fn in sorted(os.listdir(DRAFTS_DIR)):
        if not fn.endswith(".md"):
            continue
        path = os.path.join(DRAFTS_DIR, fn)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        new_text, fm_c, body_c = clean_text(text)
        if not (fm_c or body_c):
            continue
        total += 1
        slug = fn[:-3]
        tags = []
        if fm_c:
            tags.append("FM")
        if body_c:
            tags.append("正文")
        print(f"[{'+' if apply else '~'}] {slug}  (清理: {'/'.join(tags)})")
        if apply:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text)
    print(f"\n=== {'已写入' if apply else '预览'} {total} 个文件 ===")


if __name__ == "__main__":
    main()
