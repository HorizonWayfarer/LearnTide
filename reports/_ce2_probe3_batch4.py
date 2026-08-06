# -*- coding: utf-8 -*-
import re, os
D = r"A:\LearnTide\drafts"
b4 = ['gemini-free-plan-review','perplexity-ai-search-review','kling-vs-jimeng-compare',
      'jianying-ai-features-review','ai-meeting-notes-tools','ai-meeting-minutes-guide',
      'avoid-ai-hallucination-tips','jianying-ai-tutorial','suno-ai-tutorial-cn',
      'ai-mock-interview-guide']
def norm(s): return re.sub(r"\s+", "", s)
print("%-30s %-16s %3s %4s %5s %5s %5s" % ("file","pk","cnt","H2","first","last","bold"))
for n in b4:
    t = open(os.path.join(D, n+".md"), encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S); fm = m.group(1); body = t[m.end():]
    pk = re.search(r"primary_keyword:\s*(.+)", fm).group(1).strip()
    nc = re.sub(r"```.*?```", "", body, flags=re.S)
    pkn = norm(pk)
    cnt = norm(nc).count(pkn)
    h2 = [l for l in nc.split("\n") if l.startswith("## ")]
    inh2 = sum(1 for h in h2 if pkn in norm(h))
    paras = [l.strip() for l in nc.split("\n") if l.strip() and not l.startswith("#")]
    first = pkn in norm(paras[0]) if paras else False
    last = pkn in norm(paras[-1]) if paras else False
    bold = sum(1 for l in nc.split("\n") if re.match(r"^\*\*[^*]+\*\*", l.strip()))
    print("%-30s %-16s %3d %4d %5s %5s %5d" % (n[:30], pk[:16], cnt, inh2, first, last, bold))

# 链接目标真实标题
print("\n--- 内链目标标题 ---")
for s in ["tongyi-qianwen-review","claude-free-tier-limits","free-ai-tools-list",
          "chatgpt-alternatives-china","ai-video-tools-compare","how-to-write-ai-prompts",
          "notebooklm-tutorial-cn","avoid-ai-hallucination-tips","perplexity-ai-search-review",
          "what-is-llm-explained","ai-writing-tools-compare","ai-voice-tools-compare",
          "jianying-ai-features-review","kling-vs-jimeng-compare","ai-meeting-notes-tools"]:
    p = os.path.join(D, s+".md")
    if os.path.exists(p):
        t = open(p, encoding="utf-8").read()
        print("  %-30s %s" % (s, re.search(r"^title:\s*(.+)$", t, re.M).group(1)))
