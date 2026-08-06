# -*- coding: utf-8 -*-
"""Batch4 editorial probe: readability, AI-tone, structure balance."""
import re, os, json

SLUGS = [
    "gemini-free-plan-review", "perplexity-ai-search-review", "kling-vs-jimeng-compare",
    "jianying-ai-features-review", "ai-meeting-notes-tools", "ai-meeting-minutes-guide",
    "avoid-ai-hallucination-tips", "jianying-ai-tutorial", "suno-ai-tutorial-cn",
    "ai-mock-interview-guide",
]

# AI-tone red flags (Chinese cliches)
AI_CLICHE = [
    "在当今", "当今时代", "数字化时代", "众所周知", "毋庸置疑", "不言而喻",
    "值得注意的是", "综上所述", "总而言之", "总的来说", "随着.{0,8}的发展",
    "随着.{0,8}的不断", "让我们一起", "在这个", "首先.{0,30}其次.{0,30}最后",
    "无疑", "极大地", "大大提高", "赋能", "助力", "打造", "深耕", "闭环",
    "在信息爆炸", "日新月异", "层出不穷", "应运而生", "不可或缺",
    "希望本文", "本文将", "本文介绍", "相信通过", "如上所述", "由此可见",
]

PERSONA = re.compile(r"(老[陈王赵周范李张]|小[周陈梅林李方唐]|[王李张陈刘周吴徐孙马]\w{1,2}(?=老师|经理|姐))|阿玫|阿泽|王旭|周姐|李老师|小唐|老范|老赵|老周|老陈|小方|小梅|小林|小陈|小周|小李|小唐")

def split_front(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if m:
        return m.group(1), m.group(2)
    return "", text

def analyze(slug):
    p = os.path.join("drafts", slug + ".md")
    raw = open(p, encoding="utf-8").read()
    fm, body = split_front(raw)

    # strip code blocks for prose analysis
    code_blocks = re.findall(r"```.*?```", body, re.S)
    body_nocode = re.sub(r"```.*?```", "\n@@CODE@@\n", body, flags=re.S)

    lines = body_nocode.split("\n")
    prose_lines, list_lines, table_lines, head_lines = [], [], [], []
    for ln in lines:
        s = ln.strip()
        if not s or s == "@@CODE@@":
            continue
        if s.startswith("#"):
            head_lines.append(s)
        elif s.startswith("|"):
            table_lines.append(s)
        elif re.match(r"^[-*]\s|^\d+\.\s|^□", s):
            list_lines.append(s)
        else:
            prose_lines.append(s)

    prose_text = "".join(prose_lines)
    # remove markdown link syntax + inline code + bold
    prose_clean = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", prose_text)
    prose_clean = re.sub(r"\*\*|`", "", prose_clean)

    total_chars = len(re.sub(r"\s", "", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1",
                     re.sub(r"\*\*|`|\|", "", body_nocode.replace("@@CODE@@", "")))))
    prose_chars = len(prose_clean)
    list_chars = len("".join(list_lines))
    table_chars = len("".join(table_lines))
    code_chars = len("".join(code_blocks))

    # sentences (Chinese terminal punctuation)
    sents = [s for s in re.split(r"(?<=[。！？；])", prose_clean) if s.strip()]
    lens = [len(re.sub(r"\s", "", s)) for s in sents if len(re.sub(r"\s", "", s)) > 1]
    avg = sum(lens)/len(lens) if lens else 0
    short = sum(1 for l in lens if l <= 15)
    mid = sum(1 for l in lens if 16 <= l <= 30)
    lng = sum(1 for l in lens if l > 30)
    xlng = sorted([l for l in lens if l > 40], reverse=True)

    # paragraph sentence count (>4 sentences = violation)
    para_viol = []
    for ln in prose_lines:
        c = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", ln)
        n = len([x for x in re.split(r"(?<=[。！？])", c) if x.strip()])
        if n > 4:
            para_viol.append((n, c[:40]))

    # AI cliche hits
    hits = []
    for pat in AI_CLICHE:
        for m in re.finditer(pat, body):
            ctx = body[max(0, m.start()-25):m.end()+25].replace("\n", " ")
            hits.append((pat, m.group(0), ctx))

    # personas
    personas = sorted(set(PERSONA.findall(body_nocode)) | set(re.findall(
        r"(?:做\S{2,6}的|自媒体作者|研究生|行政岗的|产品经理|运营|销售岗的|律师|应届生)?(老[陈王赵周范]|小[周陈梅林李方唐]|阿玫|阿泽|王旭|周姐|李老师)", body_nocode)))
    personas = sorted({p for p in personas if p})

    # quote style
    cn_quote = len(re.findall(r"[「」]", body_nocode))
    en_quote = len(re.findall(r'"', body_nocode))
    curly = len(re.findall(r"[“”]", body_nocode))
    dash = len(re.findall(r"—{1,2}", body_nocode))
    excl = len(re.findall(r"！", prose_clean))

    # headings
    h2 = [h for h in head_lines if h.startswith("## ")]

    # primary keyword
    pk = re.search(r"primary_keyword:\s*(\S+)", fm)
    pk = pk.group(1) if pk else ""
    pk_count = body.lower().replace(" ", "").count(pk.lower().replace(" ", "")) if pk else 0
    # loose count (with spaces variant)
    pk_loose = len(re.findall("".join(re.escape(c)+r"\s*" for c in pk), body, re.I)) if pk else 0

    return dict(slug=slug, total_chars=total_chars, prose=prose_chars, lst=list_chars,
                tbl=table_chars, code=code_chars,
                prose_pct=round(100*prose_chars/max(1,total_chars),1),
                n_sent=len(lens), avg=round(avg,1), short=short, mid=mid, lng=lng,
                short_pct=round(100*short/max(1,len(lens)),1), xlng=xlng[:4],
                para_viol=para_viol, hits=hits, personas=personas,
                cn_quote=cn_quote, en_quote=en_quote, curly=curly, dash=dash, excl=excl,
                h2=len(h2), h2list=[h[3:] for h in h2], pk=pk, pk_count=pk_count, pk_loose=pk_loose,
                n_code=len(code_blocks))

out = []
for s in SLUGS:
    out.append(analyze(s))

for r in out:
    print("="*70)
    print(f"{r['slug']}  |  正文 {r['total_chars']} 字  |  H2 {r['h2']} 个  | 代码块 {r['n_code']}")
    print(f"  结构占比: 散文 {r['prose_pct']}% | 列表 {r['lst']} | 表格 {r['tbl']} | 代码 {r['code']}")
    print(f"  句子 {r['n_sent']} 句 | 平均 {r['avg']} 字 | 短(<=15) {r['short']}({r['short_pct']}%) | 中(16-30) {r['mid']} | 长(>30) {r['lng']}")
    if r['xlng']: print(f"  超长句(>40字): {r['xlng']}")
    print(f"  主词 '{r['pk']}' 出现 {r['pk_loose']} 次(宽松) / {r['pk_count']} 次(严格)")
    print(f"  具名人物: {r['personas']}")
    print(f"  引号: 「」{r['cn_quote']} / 直引号\" {r['en_quote']} / 弯引号 {r['curly']} | 破折号 {r['dash']} | 感叹号 {r['excl']}")
    if r['para_viol']:
        print(f"  !! 超 4 句段落 {len(r['para_viol'])} 处:")
        for n, t in r['para_viol']:
            print(f"       {n} 句: {t}...")
    if r['hits']:
        print(f"  !! AI 套话命中 {len(r['hits'])} 处:")
        for pat, g, ctx in r['hits']:
            print(f"       [{g}] ...{ctx}...")
    else:
        print("  AI 套话: 0 命中")
    print(f"  H2: {r['h2list']}")
