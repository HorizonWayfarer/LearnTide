# -*- coding: utf-8 -*-
"""施工后安全扫描：禁词 / ASCII引号 / 待核实 / 「」平衡 / 结尾提醒位置"""
import re, io, os
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "drafts")
out = io.StringIO()
def p(*a): out.write(" ".join(str(x) for x in a) + "\n")
files = ["wenxin-yiyan-review","midjourney-worth-subscribing","suno-ai-music-review",
         "miota-writing-cat-review","best-ai-apps-mobile",
         "ai-paper-rewrite-tips","ai-excel-tutorial","jimeng-prompt-tips","jobs-replaced-by-ai"]
BAN = ["神器","躺平","颜值飙升","暴富","随着人工智能","众所周知","毋庸置疑","SWE-bench","上下文窗口","待核实","TODO"]
for f in files:
    t = open(os.path.join(BASE, f+".md"), encoding="utf-8").read()
    body = t.split("---",2)[2]
    issues = []
    for b in BAN:
        if b.lower() in body.lower(): issues.append("禁词:"+b)
    dq = body.count('"'); sq = body.count("'")
    if dq or sq: issues.append(f"ASCII引号 双{dq} 单{sq}")
    if body.count("「") != body.count("」"): issues.append("「」不平衡")
    tail = body[-300:]
    sents = [x for x in re.split(r"[。！？\n]", tail) if x.strip()]
    last_has = ("别" in sents[-1] and "别人" not in sents[-1]) or "不要" in sents[-1]
    has_rem = "别" in tail or "不要" in tail
    p(f"{f}: {'; '.join(issues) if issues else '干净'} | 结尾提醒={'有' if has_rem else '无'} | 提醒在末句={'是' if last_has else '否'}")
with open("A:/LearnTide/reports/_batch5_safety.txt","w",encoding="utf-8") as fh:
    fh.write(out.getvalue())
