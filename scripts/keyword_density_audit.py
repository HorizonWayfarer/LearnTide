#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关键词密度审计：扫描 drafts，提取每篇 primary_keyword，
统计其在正文纯文本中的出现次数与密度（次数/中文字数*100%）。
用于判断「关键词密度修复」任务的真实缺口。

用法：
    python scripts/keyword_density_audit.py
"""
import os
import re

DRAFTS_DIR = os.path.join(os.path.dirname(__file__), "..", "drafts")
CJK = re.compile(r"[\u4e00-\u9fff]")


def parse(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        return None, text
    fm, body = m.group(1), m.group(2)
    pk = ""
    for line in fm.split("\n"):
        if line.startswith("primary_keyword:"):
            pk = line.split(":", 1)[1].strip().strip('"').strip("'")
    return pk, body


def density(pk, body):
    txt = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    txt = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", txt)
    txt = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", txt)
    txt = re.sub(r"[#*>`\-\[\]()!|:]", " ", txt)
    n = len(CJK.findall(txt))
    if not pk or n == 0:
        return 0, n, 0.0
    cnt = txt.count(pk)
    return cnt, n, cnt / n * 100


def main():
    rows = []
    for fn in sorted(os.listdir(DRAFTS_DIR)):
        if not fn.endswith(".md"):
            continue
        with open(os.path.join(DRAFTS_DIR, fn), encoding="utf-8") as f:
            text = f.read()
        pk, body = parse(text)
        cnt, n, d = density(pk, body)
        rows.append((fn[:-3], pk, cnt, n, d))
    rows.sort(key=lambda r: r[4])
    print(f"{'slug':34} {'PK':26} {'次数':>4} {'字数':>5} {'密度%':>6}")
    print("-" * 80)
    for slug, pk, cnt, n, d in rows:
        print(f"{slug:34} {pk[:24]:24} {cnt:>4} {n:>5} {d:>6.2f}")
    print("-" * 80)
    print(f"总篇数: {len(rows)}")
    print(f"密度 < 1% : {sum(1 for r in rows if r[4] < 1)} 篇")
    print(f"密度 < 0.5%: {sum(1 for r in rows if r[4] < 0.5)} 篇")
    print(f"密度 >= 2%: {sum(1 for r in rows if r[4] >= 2)} 篇")
    avg = sum(r[4] for r in rows) / len(rows)
    print(f"平均密度: {avg:.2f}%")


if __name__ == "__main__":
    main()
