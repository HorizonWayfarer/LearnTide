# -*- coding: utf-8 -*-
"""content-editor-2 Phase3 probe: readability / humanization metrics for batch4."""
import re, os, json

D = r"A:\LearnTide\drafts"
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

# AI 陈词滥调 / 机器腔
CLICHE = ["在当今", "众所周知", "随着", "值得注意的是", "毋庸置疑", "综上所述",
          "总而言之", "首先，", "其次，", "最后，", "不仅仅是", "赋能", "抓手",
          "闭环", "生态位", "数字化时代", "人工智能时代", "让我们", "总的来说",
          "不可否认", "在这个", "日新月异", "层出不穷", "至关重要", "起到了",
          "极大地", "有效地", "深刻地", "全方位", "多维度", "一站式"]
REDLINE = ["实测", "亲测", "独家", "第一手", "权威", "最全", "史上", "完爆",
           "秒杀", "遥遥领先", "颠覆", "革命性", "无敌", "绝对不会", "100%"]
HEDGE_OK = ["以官网", "以官方", "为准", "看当天", "当前说明"]

def strip_fm(t):
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    fm = m.group(1) if m else ""
    body = t[m.end():] if m else t
    return fm, body

def strip_code(b):
    fences = re.findall(r"```.*?```", b, re.S)
    return re.sub(r"```.*?```", "", b, flags=re.S), fences

rows = []
for f in FILES:
    p = os.path.join(D, f)
    t = open(p, encoding="utf-8").read()
    fm, body = strip_fm(t)
    prose_src, fences = strip_code(body)

    lines = [l.rstrip() for l in prose_src.split("\n")]
    h2 = [l for l in lines if l.startswith("## ")]
    table_lines = [l for l in lines if l.strip().startswith("|")]
    bullet_lines = [l for l in lines if re.match(r"^\s*[-*]\s+|^\s*\d+\.\s+", l)]

    # 纯散文行（排除标题/表格/列表/空行）
    prose_lines = [l for l in lines if l.strip() and not l.startswith("#")
                   and not l.strip().startswith("|") and not re.match(r"^\s*[-*]\s+|^\s*\d+\.\s+", l)]
    prose_txt = "\n".join(prose_lines)

    def han(s): return len(re.findall(r"[\u4e00-\u9fff]", s))
    total_han = han(re.sub(r"^#.*$", "", prose_src, flags=re.M))
    prose_han = han(prose_txt)
    table_han = han("\n".join(table_lines))
    bullet_han = han("\n".join(bullet_lines))
    denom = max(prose_han + table_han + bullet_han, 1)
    prose_ratio = prose_han / denom

    # 句子切分（仅散文）
    _pt = re.sub(r"[（(][^）)]*[）)]", "", prose_txt)
    sents = [s for s in re.split(r"[。！？!?]+", _pt) if han(s) >= 2]
    slen = [han(s) for s in sents]
    avg = sum(slen) / max(len(slen), 1)
    short = sum(1 for x in slen if x <= 12) / max(len(slen), 1)
    long_ = sum(1 for x in slen if x >= 35) / max(len(slen), 1)
    mx = max(slen) if slen else 0
    # 句长方差（节奏感）
    var = (sum((x - avg) ** 2 for x in slen) / max(len(slen), 1)) ** 0.5

    # 段落：连续非空散文行为一段
    paras, cur = [], []
    for l in lines:
        if not l.strip() or l.startswith("#") or l.strip().startswith("|") or re.match(r"^\s*[-*]\s+|^\s*\d+\.\s+", l):
            if cur: paras.append(" ".join(cur)); cur = []
        else:
            cur.append(l.strip())
    if cur: paras.append(" ".join(cur))
    para_sent = [len([s for s in re.split(r"[。！？!?]+", p) if han(s) >= 2]) for p in paras]
    over4 = sum(1 for x in para_sent if x > 4)

    # 段落开头多样性
    starts = [p[:3] for p in paras]
    start_dup = len(starts) - len(set(starts))

    # 具体性：人名 / 数字
    names = re.findall(r"[小老阿][\u4e00-\u9fff]|[\u4e00-\u9fff]{1,2}(?:老师|经理|姐|总)", prose_txt)
    persona = re.findall(r"(?:小|老|阿)[\u4e00-\u9fff]", prose_txt)
    nums = re.findall(r"\d+", prose_txt)
    # 迷你故事：含人物且含过去式动作词
    story_kw = re.findall(r"(踩过|吃过亏|试过|原先|后来|刚开始|事后|第二天|一次|养成)", prose_txt)

    cl = {c: prose_src.count(c) for c in CLICHE if prose_src.count(c) > 0}
    rl = {c: t.count(c) for c in REDLINE if t.count(c) > 0}
    hedge = sum(t.count(h) for h in HEDGE_OK)

    q_cjk = len(re.findall(r"「", t))
    q_curly = len(re.findall(r"[\u201c]", t))
    dashes = len(re.findall(r"——", t))

    fmd = dict(re.findall(r"^(\w+):\s*(.*)$", fm, re.M))
    rows.append(dict(
        file=f, title=fmd.get("title", ""), pk=fmd.get("primary_keyword", ""),
        mt=fmd.get("meta_title", ""), mt_len=len(fmd.get("meta_title", "")),
        md_len=len(fmd.get("meta_description", "")), lede_len=han(fmd.get("lede", "")),
        han=total_han, h2=len(h2), sents=len(slen), avg=round(avg, 1),
        short=round(short * 100), long=round(long_ * 100), maxs=mx, sd=round(var, 1),
        paras=len(paras), over4=over4, start_dup=start_dup,
        prose_ratio=round(prose_ratio * 100), table=len(table_lines), bullet=len(bullet_lines),
        fences=len(fences), persona=len(set(persona)), nums=len(nums), story=len(story_kw),
        cliche=cl, redline=rl, hedge=hedge, q_cjk=q_cjk, q_curly=q_curly, dash=dashes,
    ))

hdr = ["file", "han", "h2", "sents", "avg", "short", "long", "maxs", "sd", "paras", "over4",
       "start_dup", "prose_ratio", "table", "bullet", "fences", "persona", "nums", "story",
       "hedge", "q_cjk", "q_curly", "dash", "mt_len", "md_len", "lede_len"]
print("\t".join(hdr))
for r in rows:
    print("\t".join(str(r[k]) for k in hdr))
print("\n=== CLICHE / REDLINE ===")
for r in rows:
    print(f"{r['file']}\n  cliche={r['cliche']}\n  redline={r['redline']}")
