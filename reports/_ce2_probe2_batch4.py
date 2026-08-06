# -*- coding: utf-8 -*-
import re, os
D = r"A:\LearnTide\drafts"
FILES = ["gemini-free-plan-review.md","perplexity-ai-search-review.md","kling-vs-jimeng-compare.md",
         "jianying-ai-features-review.md","ai-meeting-notes-tools.md","ai-meeting-minutes-guide.md",
         "avoid-ai-hallucination-tips.md","jianying-ai-tutorial.md","suno-ai-tutorial-cn.md",
         "ai-mock-interview-guide.md"]
def han(s): return len(re.findall(r"[\u4e00-\u9fff]", s))
for f in FILES:
    t = open(os.path.join(D,f), encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S); fm=m.group(1); body=t[m.end():]
    nocode = re.sub(r"```.*?```","",body,flags=re.S)
    print("="*70); print(f)
    # 引号风格
    print("  quotes: 「=%d 」=%d U+201C=%d U+201D=%d ascii\"=%d '=%d ——=%d …=%d"
          % (t.count("\u300c"),t.count("\u300d"),t.count("\u201c"),t.count("\u201d"),
             t.count('"'),t.count("\u2018"),t.count("\u2014\u2014"),t.count("\u2026")))
    # front-matter links vs body links
    fml = re.findall(r"-\s+(?:slug|path):\s*(\S+)\n\s+anchor:\s*(.+)", fm)
    bl  = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", nocode)
    print("  FM links:", [(a.strip(), s) for s,a in fml])
    print("  BODY links:", bl)
    fm_t = {s.replace('.html','') for s,a in fml}
    bd_t = {u.replace('.html','').replace('../','') for _,u in bl}
    print("  FM-only:", sorted(fm_t - bd_t - {'../tools.html'}), " BODY-only:", sorted(bd_t - {x.replace('.html','') for x in fm_t}))
    # anchor 文案是否一致
    for a,u in bl:
        for s,fa in fml:
            if s.replace('.html','')==u.replace('.html','') and fa.strip()!=a:
                print(f"  !! anchor mismatch [{u}] FM='{fa.strip()}' BODY='{a}'")
    # 最长句子 top3
    prose=[l.strip() for l in nocode.split("\n") if l.strip() and not l.startswith("#")
           and not l.strip().startswith("|") and not re.match(r"^\s*[-*]\s+|^\s*\d+\.\s+",l)]
    sents=[s for s in re.split(r"(?<=[。！？])", " ".join(prose)) if han(s)>=2]
    top=sorted(sents,key=lambda s:-han(s))[:3]
    for s in top: print(f"  LONG({han(s)}): {s.strip()[:90]}")
    # 段落开头重复
    starts=[p[:4] for p in prose]
    dup={s:starts.count(s) for s in set(starts) if starts.count(s)>1}
    if dup: print("  para-start dup:", dup)
    # 全角/半角、空格规范
    if re.search(r"[\u4e00-\u9fff]\s+[\u4e00-\u9fff]", nocode): print("  !! 中文间多余空格")
    bad=re.findall(r"[\u4e00-\u9fff][A-Za-z0-9]|[A-Za-z0-9][\u4e00-\u9fff]", nocode)
    print("  中英无空格处 n=%d 例:%s" % (len(bad), bad[:6]))
