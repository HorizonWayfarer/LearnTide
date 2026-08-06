# -*- coding: utf-8 -*-
"""施工自测：H2 关键词保留 + 结尾提醒位置 + 可读性复核。只读不写。"""
import re, io, sys, os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "drafts")
out = io.StringIO()
def p(*a):
    out.write(" ".join(str(x) for x in a) + "\n")

files = ["wenxin-yiyan-review","midjourney-worth-subscribing","suno-ai-music-review",
         "miota-writing-cat-review","best-ai-apps-mobile",
         "ai-paper-rewrite-tips","ai-excel-tutorial","jimeng-prompt-tips","jobs-replaced-by-ai"]

for f in files:
    t = open(os.path.join(BASE, f + ".md"), encoding="utf-8").read()
    fm, body = t.split("---",2)[1], t.split("---",2)[2]
    nocode = re.sub(r"```.*?```", "", body, flags=re.S)
    kw = re.search(r"primary_keyword: (.+)", fm).group(1).strip().lower()
    h2s = re.findall(r"^## (.+)$", body, flags=re.M)
    kwin = [kw in re.sub(r"[\s]","",h).lower() for h in h2s]
    # 结尾提醒位置
    tail = nocode[-300:]
    sents = [x for x in re.split(r"[。！？\n]", tail) if x.strip()]
    last_has = ("别" in sents[-1] and "别人" not in sents[-1]) or "不要" in sents[-1]
    has_rem = "别" in tail or "不要" in tail
    # 最后一句是否含主词
    last_sent_kw = kw in re.sub(r"[\s]","",sents[-1]).lower()
    # 可读性
    paras = [x for x in nocode.split("\n\n") if x.strip() and not x.strip().startswith(("#","|",">","```"))]
    lens=[]
    for pp in paras:
        for s in re.split(r"[。！？]", pp):
            n = len(re.findall(r"[\u4e00-\u9fff]", s))
            if n>0: lens.append(n)
    avg = sum(lens)/len(lens) if lens else 0
    ratio = sum(1 for x in lens if x<=12)/len(lens)*100 if lens else 0
    p(f"== {f} | kw='{kw}' | H2含KW={sum(kwin)}/{len(h2s)} | 结尾提醒={'有' if has_rem else '无'} | 提醒在末句={'是' if last_has else '否'} | 末句含主词={'是' if last_sent_kw else '否'} | 均句长{avg:.1f} | 短句{ratio:.0f}%")

with open("A:/LearnTide/reports/_batch5_construction_selftest.txt","w",encoding="utf-8") as fh:
    fh.write(out.getvalue())
print("DONE")
