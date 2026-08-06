# -*- coding: utf-8 -*-
"""第四批 10 篇页面 SEO 探针（欧化成）。只读，不改稿，不属于交付物。

输出：关键词密度/分布、H2/H3 结构、meta 宽度、内外链、表格/列表/代码块、
可读性（均句长、短句占比、段落长度）、精选摘要可捕获结构判定。
"""
import re, os, sys, json

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "drafts")
A = os.path.join(ROOT, "articles")

SLUGS = [
    "gemini-free-plan-review", "perplexity-ai-search-review",
    "kling-vs-jimeng-compare", "jianying-ai-features-review",
    "ai-meeting-notes-tools", "ai-meeting-minutes-guide",
    "avoid-ai-hallucination-tips", "jianying-ai-tutorial",
    "suno-ai-tutorial-cn", "ai-mock-interview-guide",
]

# 每篇的语义变体 / LSI（人工圈定，用于覆盖度检查）
LSI = {
    "gemini-free-plan-review": ["gemini", "免费版", "免费额度", "付费", "多模态", "降档", "谷歌"],
    "perplexity-ai-search-review": ["perplexity", "ai搜索", "来源", "引用", "检索", "免费档", "付费"],
    "kling-vs-jimeng-compare": ["可灵", "即梦", "文生视频", "图生视频", "积分", "提示词", "口型"],
    "jianying-ai-features-review": ["剪映", "智能字幕", "智能成片", "数字人", "会员", "降噪", "口播"],
    "ai-meeting-notes-tools": ["会议纪要", "转写", "飞书妙记", "通义听悟", "腾讯会议", "说话人", "待办"],
    "ai-meeting-minutes-guide": ["会议纪要", "逐字稿", "转写", "待办", "责任人", "提示词", "录音"],
    "avoid-ai-hallucination-tips": ["幻觉", "编造", "核对", "交叉验证", "来源", "不确定", "提示词"],
    "jianying-ai-tutorial": ["剪映", "智能成片", "自动字幕", "文本朗读", "口播", "模板", "导出"],
    "suno-ai-tutorial-cn": ["suno", "歌词", "风格", "咬字", "副歌", "结构标签", "免费额度"],
    "ai-mock-interview-guide": ["模拟面试", "面试官", "追问", "提示词", "复盘", "jd", "简历"],
}


def width(s):
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


def norm(x):
    return re.sub(r"[\s\u3000]", "", x).lower()


def cjk(s):
    return len(re.findall(r"[\u4e00-\u9fff]", s))


rows = []
for slug in SLUGS:
    raw = open(os.path.join(D, slug + ".md"), encoding="utf-8").read()
    fm, body = raw.split("---", 2)[1], raw.split("---", 2)[2]
    nocode = re.sub(r"```.*?```", "", body, flags=re.S)

    def f(k, src=fm):
        m = re.search(r"^%s: (.+)$" % k, src, flags=re.M)
        return m.group(1).strip() if m else ""

    kw = f("primary_keyword")
    kwn = norm(kw)
    mt, md, lede = f("meta_title"), f("meta_description"), f("lede")
    atype = f("article_type")

    total_cjk = cjk(nocode)
    # 关键词出现次数（正文，剥空格后匹配）
    flat = norm(nocode)
    occ = flat.count(kwn)
    # 字符法密度：命中的汉字数 / 正文汉字总数（分子分母口径一致，不含拉丁字母）
    dens = occ * max(cjk(kw), 1) / max(total_cjk, 1) * 100

    h2s = re.findall(r"^## (.+)$", body, flags=re.M)
    h3s = re.findall(r"^### (.+)$", body, flags=re.M)
    h2_hit = [h for h in h2s if kwn in norm(h)]

    # 首段：第一段正文（跳过第一个 H2）
    paras = [p.strip() for p in nocode.split("\n\n") if p.strip()]
    prose = [p for p in paras if not p.startswith(("#", "|", ">", "-", "```", "□"))]
    first_para = prose[0] if prose else ""
    first100 = norm(nocode.strip())[:130]
    last_para = prose[-1] if prose else ""

    # 链接
    inline_links = re.findall(r"\[([^]]+)\]\(([^)]+)\)", nocode)
    internal_inline = [l for l in inline_links if not l[1].startswith("http")]
    external_inline = [l for l in inline_links if l[1].startswith("http")]
    fm_links = len(re.findall(r"^  - (?:slug|path):", fm, flags=re.M))

    has_table = "\n|" in nocode
    table_rows = len([l for l in nocode.split("\n") if l.strip().startswith("|")])
    code_blocks = len(re.findall(r"^```", body, flags=re.M)) // 2
    bullets = len([l for l in nocode.split("\n") if re.match(r"^\s*[-*] ", l)])
    numbered = len([l for l in nocode.split("\n") if re.match(r"^\s*\d+\. ", l)])
    bold = len(re.findall(r"\*\*[^*]+\*\*", nocode))

    # 可读性
    sent_lens = []
    for p in prose:
        for s in re.split(r"[。！？]", p):
            n = cjk(s)
            if n:
                sent_lens.append(n)
    avg = sum(sent_lens) / max(len(sent_lens), 1)
    short = sum(1 for x in sent_lens if x <= 12) / max(len(sent_lens), 1) * 100
    para_lens = [cjk(p) for p in prose]
    long_paras = [n for n in para_lens if n > 120]

    # LSI 覆盖
    lsi = LSI[slug]
    lsi_hit = [t for t in lsi if t in flat]

    # H2 疑问句 / 步骤式（精选摘要判定）
    q_h2 = [h for h in h2s if "？" in h or "?" in h]
    step_h2 = [h for h in h2s if re.search(r"第[一二三四五六]步|步走|轮|习惯[一二三四五]", h)]

    # 构建产物核对
    html_p = os.path.join(A, slug + ".html")
    html = open(html_p, encoding="utf-8").read() if os.path.exists(html_p) else ""
    h1 = re.search(r"<h1>(.*?)</h1>", html)
    ld_types = re.findall(r'"@type":"(\w+)"', html)
    html_title = re.search(r"<title>(.*?)</title>", html)
    html_desc = re.search(r'<meta name="description" content="(.*?)"', html)
    related = len(re.findall(r'相关阅读', html))
    rel_items = re.search(r"相关阅读</h4>\s*<ul>(.*?)</ul>", html, flags=re.S)
    rel_n = len(re.findall(r"<li>", rel_items.group(1))) if rel_items else 0

    rows.append(dict(
        slug=slug, atype=atype, kw=kw, cjk=total_cjk, occ=occ, dens=round(dens, 2),
        h2=len(h2s), h3=len(h3s), h2_kw=len(h2_hit), h2_list=h2s,
        kw_first100=kwn in first100,
        kw_first_para=kwn in norm(first_para),
        kw_last=kwn in norm(last_para),
        kw_mt=kwn in norm(mt), kw_md=kwn in norm(md), kw_lede=kwn in norm(lede),
        mt_w=width(mt), mt_c=len(mt), md_w=width(md), md_c=len(md),
        inline_int=len(internal_inline), inline_ext=len(external_inline),
        fm_links=fm_links, rel_n=rel_n,
        table=table_rows, code=code_blocks, bullets=bullets, numbered=numbered, bold=bold,
        avg=round(avg, 1), short=round(short), paras=len(prose),
        maxpara=max(para_lens) if para_lens else 0, longparas=len(long_paras),
        lsi_hit=len(lsi_hit), lsi_total=len(lsi), lsi_miss=[t for t in lsi if t not in flat],
        q_h2=len(q_h2), step_h2=len(step_h2),
        h1=h1.group(1) if h1 else "", ld=sorted(set(ld_types)),
        title_ok=bool(html_title and html_title.group(1) == mt),
        desc_ok=bool(html_desc and html_desc.group(1) == md),
        anchors=[a for a, _ in internal_inline],
    ))

print(json.dumps(rows, ensure_ascii=False, indent=1))
