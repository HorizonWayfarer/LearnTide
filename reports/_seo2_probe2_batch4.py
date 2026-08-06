# -*- coding: utf-8 -*-
"""Batch-4 deep probe: meta char widths, kw positions, snippet-format readiness, cannibalization."""
import os, re, json, unicodedata, itertools

DRAFTS = r"A:/LearnTide/drafts"
B4 = ["gemini-free-plan-review","perplexity-ai-search-review","kling-vs-jimeng-compare",
      "jianying-ai-features-review","ai-meeting-notes-tools","ai-meeting-minutes-guide",
      "avoid-ai-hallucination-tips","jianying-ai-tutorial","suno-ai-tutorial-cn",
      "ai-mock-interview-guide"]

def norm(s):
    return re.sub(r"[\s\u3000\-_—·/、，,。.？?！!：:；;（）()\[\]【】\"'“”‘’]", "", s.lower())

def fm_of(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    fm, cur = {}, None
    for line in m.group(1).split("\n"):
        mm = re.match(r"^(\w+):\s*(.*)$", line)
        if mm and not line.startswith(" "):
            fm[mm.group(1)] = mm.group(2).strip()
    return fm, m.group(2)

print("=== META LENGTH (CJK-aware) ===")
print(f"{'slug':30}{'MT_ch':>6}{'MT_px~':>7}{'MD_ch':>6}{'MD_px~':>7}{'H1_ch':>6}")
rows = {}
for s in B4:
    fm, body = fm_of(os.path.join(DRAFTS, s + ".md"))
    rows[s] = (fm, body)
    mt, md, ti = fm.get("meta_title",""), fm.get("meta_description",""), fm.get("title","")
    # approx pixel: CJK ~ 2 units, latin ~1  (Google SERP: title ~600px≈ 30 CJK; desc ~960px ≈ 78 CJK)
    px = lambda x: sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in x)
    print(f"{s:30}{len(mt):>6}{px(mt):>7}{len(md):>6}{px(md):>7}{len(ti):>6}")

print("\n=== KEYWORD OCCURRENCE POSITIONS ===")
for s in B4:
    fm, body = rows[s]
    kw = fm["primary_keyword"]; nk = norm(kw)
    lines = body.split("\n")
    hits = []
    for i, ln in enumerate(lines):
        if nk in norm(ln):
            kind = "H2" if ln.startswith("## ") else ("H3" if ln.startswith("### ") else "P")
            hits.append(f"L{i+1}/{kind}")
    print(f"{s:30} kw={kw:18} -> {', '.join(hits)}")

print("\n=== STRUCTURE / SNIPPET READINESS ===")
print(f"{'slug':30}{'H1':>4}{'H2':>4}{'H3':>4}{'tbl':>5}{'ul':>4}{'ol':>4}{'code':>5}{'faq?':>6}{'defP':>6}")
for s in B4:
    fm, body = rows[s]
    h1 = len(re.findall(r"^#\s+", body, re.M))
    h2 = len(re.findall(r"^##\s+", body, re.M))
    h3 = len(re.findall(r"^###\s+", body, re.M))
    tbl = len(re.findall(r"^\|\s*-{2,}", body, re.M))
    ul = len(re.findall(r"^[-*]\s", body, re.M))
    ol = len(re.findall(r"^\d+\.\s", body, re.M))
    code = len(re.findall(r"^```", body, re.M))//2
    q_h2 = sum(1 for h in re.findall(r"^##\s+(.*)$", body, re.M) if ("？" in h or "?" in h or "怎么" in h or "如何" in h))
    # definition paragraph: a paragraph <=120 chars right after a question H2
    print(f"{s:30}{h1:>4}{h2:>4}{h3:>4}{tbl:>5}{ul:>4}{ol:>4}{code:>5}{q_h2:>6}{'-':>6}")

print("\n=== H2 OUTLINES ===")
for s in B4:
    fm, body = rows[s]
    print(f"\n[{s}]  kw={fm['primary_keyword']}")
    for h in re.findall(r"^##\s+(.*)$", body, re.M):
        mark = "*" if norm(fm['primary_keyword']) in norm(h) else " "
        print(f"   {mark} {h}")

print("\n=== IN-BODY LINKS ===")
for s in B4:
    fm, body = rows[s]
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", body)
    print(f"{s:30} inbody={len(links):<3} {[l[1] for l in links]}")

print("\n=== FRONT-MATTER DECLARED LINKS vs IN-BODY ===")
for s in B4:
    raw = open(os.path.join(DRAFTS, s+".md"), encoding="utf-8").read()
    fmraw = re.match(r"^---\n(.*?)\n---\n", raw, re.S).group(1)
    decl = re.findall(r"(?:slug|path):\s*(\S+)", fmraw)
    decl = [d for d in decl if d != s]
    body = raw.split("---\n",2)[2]
    inbody = [l for _, l in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", body)]
    inbody_slugs = [re.sub(r"\.html$","",x).split("/")[-1] for x in inbody]
    missing = [d for d in decl if re.sub(r"\.html$","",d).split("/")[-1] not in inbody_slugs]
    print(f"{s:30} declared={len(decl)} inbody={len(inbody)} NOT_IN_BODY={missing}")

print("\n=== CANNIBALIZATION MATRIX (batch4 internal + vs existing drafts) ===")
allfiles = [f[:-3] for f in os.listdir(DRAFTS) if f.endswith(".md")]
kws = {}
for f in allfiles:
    try:
        fm, _ = fm_of(os.path.join(DRAFTS, f+".md"))
        kws[f] = fm.get("primary_keyword","")
    except Exception:
        pass
def jac(a,b):
    A=set(norm(a)); B=set(norm(b))
    return len(A&B)/max(len(A|B),1)
pairs=[]
for a in B4:
    for b in allfiles:
        if a==b: continue
        j = jac(kws.get(a,""), kws.get(b,""))
        ts = jac(a.replace("-",""), b.replace("-",""))
        score = max(j, ts*0.9)
        if score >= 0.42:
            pairs.append((round(score,2), a, kws.get(a), b, kws.get(b)))
for p in sorted(pairs, reverse=True):
    print(f"  {p[0]:<5} {p[1]}({p[2]})  <->  {p[3]}({p[4]})")
