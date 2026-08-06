#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一次性修复：把 drafts 中标题行（# 开头）里的 markdown 外链还原为纯文本。
正文里的外链保持不变。
用途：add_external_links.py 早期版本误把标题行也加了链接，本脚本修正。
"""
import os
import re
import sys

DRAFTS_DIR = os.path.join(os.path.dirname(__file__), "..", "drafts")
LINK_PAT = re.compile(r"\[([^\]]+)\]\(https?://[^)]+\)\{:target=\"_blank\"\}")

def main():
    slugs = [l.strip() for l in sys.stdin if l.strip()]
    fixed = 0
    for slug in slugs:
        path = os.path.join(DRAFTS_DIR, slug + ".md")
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().split("\n")
        changed = False
        for i, line in enumerate(lines):
            if re.match(r"^#{1,6}\s", line):
                new = LINK_PAT.sub(r"\1", line)
                if new != line:
                    lines[i] = new
                    changed = True
        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            fixed += 1
            print(f"[fix] {slug}")
    print(f"\n=== 修复 {fixed} 篇标题 ===")

if __name__ == "__main__":
    main()
