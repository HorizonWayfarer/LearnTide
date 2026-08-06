# -*- coding: utf-8 -*-
import re, glob, os, collections
D = r"A:\LearnTide\drafts"
m = collections.defaultdict(list)
for p in sorted(glob.glob(os.path.join(D, "*.md"))):
    t = open(p, encoding="utf-8").read()
    fm = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    if not fm:
        continue
    n = os.path.basename(p)[:-3]
    for s, a in re.findall(r"-\s+slug:\s*(\S+)\n\s+anchor:\s*(.+)", fm.group(1)):
        m[s].append((n, a.strip()))

for tgt in ["how-to-write-ai-prompts", "avoid-ai-hallucination-tips",
            "kling-vs-jimeng-compare", "perplexity-ai-search-review",
            "ai-meeting-minutes-guide", "jianying-ai-tutorial",
            "ai-mock-interview-guide", "gemini-free-plan-review",
            "suno-ai-tutorial-cn", "ai-resume-optimization",
            "tongyi-qianwen-review"]:
    lst = m.get(tgt, [])
    print("== %s  (FM 入链 %d)" % (tgt, len(lst)))
    c = collections.Counter(a for _, a in lst)
    for src, a in lst:
        print("   %-32s %s%s" % (src, a, "   <== 碰撞" if c[a] > 1 else ""))
    if not lst:
        print("   (无 FM 入链声明 = 孤岛)")
