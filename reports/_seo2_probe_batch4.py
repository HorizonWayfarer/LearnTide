# -*- coding: utf-8 -*-
"""Batch-4 on-page SEO quantitative probe (seo-optimizer-2, independent audit)."""
import os, re, json, unicodedata

DRAFTS = r"A:/LearnTide/drafts"
FILES = [
    "gemini-free-plan-review.md",
    "perplexity-ai-search-review.md",
    "kling-vs-jimeng-compare.md",
    "jianying-ai-features-review.md",
    "ai-meeting-notes-tools.md",
    "ai-meeting-minutes-guide.md",
    "avoid-ai-hallucination-tips.md",
    "jianying-ai-tutorial.md",
    "suno-ai-tutorial-cn.md",
    "ai-mock-interview-guide.md",
]

def visual_len(s):
    """Meta length as SERP-ish width: CJK=2, ASCII=1 -> return both raw & width."""
    w = 0
    for ch in s:
        w += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return len(s), w

def norm(s):
    s = s.lower()
    s = re.sub(r"[\s\u3000\-_—·/、，,。.？?！!：:；;（）()\[\]【】\"'“”‘’]", "", s)
    return s

def parse(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    fm_raw, body = m.group(1), m.group(2)
    fm = {}
    cur = None
    ilinks = []
    for line in fm_raw.split("\n"):
        if re.match(r"^\s*-\s", line) or re.match(r"^\s{2,}\w+:", line):
            if cur == "internal_links":
                mm = re.search(r"(slug|path):\s*(.+)", line)
                if mm:
                    ilinks.append({"target": mm.group(2).strip()})
                mm2 = re.search(r"anchor:\s*(.+)", line)
                if mm2 and ilinks:
                    ilinks[-1]["anchor"] = mm2.group(1).strip()
            continue
        mm = re.match(r"^(\w+):\s*(.*)$", line)
        if mm:
            cur = mm.group(1)
            fm[cur] = mm.group(2).strip()
    fm["internal_links"] = ilinks
    return fm, body

def analyze(fn):
    fm, body = parse(os.path.join(DRAFTS, fn))
    kw = fm.get("primary_keyword", "")
    nk = norm(kw)

    # strip code fences for prose stats, keep for structure stats
    code_blocks = re.findall(r"```.*?```", body, re.S)
    prose = re.sub(r"```.*?```", "", body, flags=re.S)

    # headings
    h2 = re.findall(r"^##\s+(.*)$", body, re.M)
    h3 = re.findall(r"^###\s+(.*)$", body, re.M)

    # links
    md_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", body)
    internal_inline = [l for l in md_links if not l[1].startswith("http")]
    external_inline = [l for l in md_links if l[1].startswith("http")]

    # char counts
    cn_chars = len(re.findall(r"[\u4e00-\u9fff]", prose))
    total_chars = len(re.sub(r"\s", "", prose))

    # keyword occurrences (normalized, whole body prose)
    nprose = norm(prose)
    occ_body = nprose.count(nk) if nk else 0
    # first 100 chars of prose (after removing headings markup)
    plain = re.sub(r"^#+\s*", "", prose, flags=re.M)
    plain = re.sub(r"\s+", "", plain)
    first100 = plain[:100]
    in_first100 = nk in norm(first100)
    # first paragraph after first H2
    in_title = nk in norm(fm.get("title", ""))
    in_meta_title = nk in norm(fm.get("meta_title", ""))
    in_meta_desc = nk in norm(fm.get("meta_description", ""))
    in_lede = nk in norm(fm.get("lede", ""))
    in_slug_kw = None
    h2_hits = sum(1 for h in h2 if nk in norm(h))
    # conclusion = last 2 paragraphs
    paras = [p for p in prose.strip().split("\n\n") if p.strip()]
    tail = norm("".join(paras[-2:]))
    in_conclusion = nk in tail

    density = round(occ_body * len(nk) / total_chars * 100, 2) if total_chars else 0

    mt_len, mt_w = visual_len(fm.get("meta_title", ""))
    md_len, md_w = visual_len(fm.get("meta_description", ""))
    t_len, t_w = visual_len(fm.get("title", ""))

    return {
        "file": fn,
        "slug": fm.get("slug"),
        "title": fm.get("title"),
        "type": fm.get("article_type"),
        "category": fm.get("category"),
        "primary_keyword": kw,
        "cn_chars": cn_chars,
        "total_chars_nospace": total_chars,
        "h2_count": len(h2),
        "h3_count": len(h3),
        "h2_list": h2,
        "kw_occ_body": occ_body,
        "kw_density_pct": density,
        "kw_in_title": in_title,
        "kw_in_meta_title": in_meta_title,
        "kw_in_meta_desc": in_meta_desc,
        "kw_in_lede": in_lede,
        "kw_in_first100": in_first100,
        "kw_in_h2_count": h2_hits,
        "kw_in_conclusion": in_conclusion,
        "meta_title": fm.get("meta_title"),
        "meta_title_chars": mt_len,
        "meta_title_width": mt_w,
        "meta_desc": fm.get("meta_description"),
        "meta_desc_chars": md_len,
        "meta_desc_width": md_w,
        "title_chars": t_len,
        "title_width": t_w,
        "fm_internal_links": fm["internal_links"],
        "inline_internal_links": internal_inline,
        "inline_internal_count": len(internal_inline),
        "external_links": external_inline,
        "external_count": len(external_inline),
        "tables": body.count("\n|---") + body.count("\n|--- "),
        "has_table": "|---" in body,
        "code_blocks": len(code_blocks),
        "bullet_lines": len(re.findall(r"^[-*]\s", prose, re.M)),
        "bold_count": len(re.findall(r"\*\*[^*]+\*\*", prose)),
        "para_count": len(paras),
        "avg_para_chars": round(sum(len(re.sub(r'\s','',p)) for p in paras)/max(len(paras),1)),
    }

out = [analyze(f) for f in FILES]
open(r"A:/LearnTide/reports/_seo2_probe_batch4.json", "w", encoding="utf-8").write(
    json.dumps(out, ensure_ascii=False, indent=2))

hdr = f"{'slug':32}{'kw_occ':>7}{'dens%':>7}{'chars':>7}{'H2':>4}{'kwH2':>6}{'f100':>6}{'concl':>7}{'mt_w':>6}{'md_w':>6}{'inLnk':>6}{'ext':>5}{'tbl':>5}{'code':>5}"
print(hdr)
print("-"*len(hdr))
for r in out:
    print(f"{r['slug']:32}{r['kw_occ_body']:>7}{r['kw_density_pct']:>7}{r['total_chars_nospace']:>7}"
          f"{r['h2_count']:>4}{r['kw_in_h2_count']:>6}{str(r['kw_in_first100']):>6}"
          f"{str(r['kw_in_conclusion']):>7}{r['meta_title_width']:>6}{r['meta_desc_width']:>6}"
          f"{r['inline_internal_count']:>6}{r['external_count']:>5}{str(r['has_table']):>5}{r['code_blocks']:>5}")
