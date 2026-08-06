# -*- coding: utf-8 -*-
"""Batch4 probe 2: locate over-long sentences + quote char audit."""
import re, os

SLUGS = ["gemini-free-plan-review","perplexity-ai-search-review","kling-vs-jimeng-compare",
 "jianying-ai-features-review","ai-meeting-notes-tools","ai-meeting-minutes-guide",
 "avoid-ai-hallucination-tips","jianying-ai-tutorial","suno-ai-tutorial-cn",
 "ai-mock-interview-guide"]

print("### 一、引号字符审计（U+201C/201D 弯引号 vs U+0022 直引号 vs 「」）")
for s in SLUGS:
    raw = open(os.path.join("drafts", s+".md"), encoding="utf-8").read()
    body = raw.split("---",2)[2] if raw.startswith("---") else raw
    body_nc = re.sub(r"```.*?```","",body,flags=re.S)
    c = {
      "「」": len(re.findall(r"[\u300c\u300d]", body_nc)),
      "“”(U+201C/D)": len(re.findall(r"[\u201c\u201d]", body_nc)),
      '"(U+0022)': len(re.findall(r"\u0022", body_nc)),
      "''": len(re.findall(r"[\u2018\u2019]", body_nc)),
    }
    print(f"  {s:34s} " + " | ".join(f"{k}={v}" for k,v in c.items()))

print()
print("### 二、超长句定位（>38 字，去空白计）")
for s in SLUGS:
    raw = open(os.path.join("drafts", s+".md"), encoding="utf-8").read()
    lines = raw.split("\n")
    incode=False; found=[]
    for i,ln in enumerate(lines,1):
        if ln.strip().startswith("```"): incode = not incode; continue
        if incode: continue
        t=ln.strip()
        if not t or t.startswith("#") or t.startswith("|") or re.match(r"^[-*]\s|^\d+\.\s|^□",t): continue
        if ":" in t and i<25: continue
        c = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
        c = re.sub(r"\*\*|`","",c)
        for sent in re.split(r"(?<=[。！？])", c):
            n=len(re.sub(r"\s","",sent))
            if n>38: found.append((i,n,sent.strip()))
    if found:
        print(f"\n  --- {s} ---")
        for i,n,t in found: print(f"    L{i} ({n}字): {t}")

print()
print("### 三、每篇开场首句（钩子强度检查）")
for s in SLUGS:
    raw = open(os.path.join("drafts", s+".md"), encoding="utf-8").read()
    lead = re.search(r"^lede:\s*(.+)$", raw, re.M)
    body = raw.split("---",2)[2]
    first = [l.strip() for l in body.split("\n") if l.strip() and not l.strip().startswith("#")][0]
    first = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", first)
    print(f"\n  {s}")
    print(f"    lede : {lead.group(1) if lead else '—'}")
    print(f"    首句 : {first[:70]}")

print()
print("### 四、结尾句 + 免责声明检查")
for s in SLUGS:
    raw = open(os.path.join("drafts", s+".md"), encoding="utf-8").read()
    body = raw.split("---",2)[2]
    paras=[l.strip() for l in body.split("\n") if l.strip()]
    disc = any(("以官网" in p or "官网当天" in p or "官方条款" in p or "定价页" in p or "官网说明" in p or "说明页" in p) for p in paras)
    print(f"  {s:34s} 免责声明={'有' if disc else '【缺】'} | 尾句: {paras[-1][:52]}")

print()
print("### 五、内链落实 vs brief 建议")
for s in SLUGS:
    raw = open(os.path.join("drafts", s+".md"), encoding="utf-8").read()
    fm = raw.split("---",2)[1]
    body = raw.split("---",2)[2]
    declared = re.findall(r"(?:slug|path):\s*(\S+)", fm)
    inbody = re.findall(r"\]\(([^)]+)\)", body)
    inbody = [x.replace(".html","") for x in inbody]
    missing=[d for d in declared if d not in inbody and d.replace("../","").replace(".html","") not in inbody and "tools" not in d]
    print(f"  {s:34s} 声明{len(declared)} 正文出现{len(inbody)} | 声明未落地: {missing}")
