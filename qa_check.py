# -*- coding: utf-8 -*-
"""稿件交付自检。可重复运行，适用于全部 100 篇。

检查分两档，输出里分开标记：
  FAIL —— 硬性交付标准。必须全部通过，否则不算完成。
  WARN —— 质量基线。不阻塞交付，由编辑判断值不值得改。

────── 硬失败项 1-9（2026-08-04 之前即在用）──────
  H2 4-5 个、至少 1 个代码块、关键词三处覆盖（首段/H2/结尾）、
  front-matter 必填字段、无 emoji、无禁词、正文无手写 Markdown 链接、无 H1、
  内链 3-5 条且 path 合法、meta 标题与描述宽度、lede 字数、结尾反向提醒。
  【字数按 article_type 分档，见下方「字数分档」一节 —— 仍是硬失败，只是区间随类型变。】

────── 2026-08-04 追加项 10-14（第 1 批编辑复盘，content-editor 提出，team-lead 采纳）──────

10) lede 与正文连续重合 ≥8 字 —— FAIL
    依据：第 1 批 10 篇原稿有 9 篇的 lede 与正文近乎逐字重复。lede 渲染在正文
    正上方，读者三秒内会看到同一句话两遍。这是任何 SEO 检查都发现不了、真实
    读者却一眼就烦的问题，且 100% 属于撰稿疏漏，没有「可以商量」的余地，所以
    定为硬失败。
    阈值 8 的来历：比较前先剥掉标点和空格，只留下文字本身。剥完之后 8 个连续
    字符已经构成一个可独立成立的短句（如「你有没有长资料要读」）；6-7 字则多为
    术语枚举（如「选题、标题、正文」剥标点后只剩 6 字），属于正常复用，不该误报。
    剥标点这一步是必要的：不剥的话，带顿号的三词枚举会凑够 8 字被误判。

11) 短句（≤12 字）占比 ≥15% —— WARN
    依据：第 1 批原稿有 2 篇短句占比为 0%，通篇 25-30 字长句连排，中文读到第三个
    长句就开始滑眼。编辑后全批从 9% 提到 16%，读感明显改善，故取 15% 作下限。
    定为 WARN 而非 FAIL：硬卡这个数会诱导为凑指标写出机械短句，反而更像 AI。
    指标不达标时应当回看长句能不能自然拆开，而不是硬塞短句。

12) 平均句长 ≤26 字 —— WARN
    依据：中文网络长文的舒适区是 22-26 字/句。第 1 批原稿全批均值 27.2 字，编辑后
    24.3 字。同样定为 WARN，理由与 11) 相同。
    注：11) 和 12) 只统计正文散文段落，跳过标题、表格、引用块和代码块。

13) 同一免责措辞每篇最多 1 次 —— WARN
    依据：「以官网当前说明为准」在第 1 批某篇里出现了 3 次。免责本身是本站「说真话」
    定位的一部分，必须保留，但同一句话复读会显得敷衍。改法是换措辞而不是删免责，
    例如「掏钱前去官网定价页扫一眼」「具体权益去官网会员页看」。

14) 「不是 A，是 B」句式每篇最多 1 处 —— WARN
    依据：这个句式很好用，但第 1 批有一篇连用 3 次，通篇像同一个模具压出来的，是
    典型的 AI 文风特征。每篇留 1 处最有力的（通常是题眼句），其余改写。

────── 字数分档（2026-08-04 追加，伟超批，content-editor 诊断推动）──────
  字数仍是硬失败，但区间不再写死，而是读 front-matter 的 article_type 字段，
  按不同文章类型套不同下限/上限：

    article_type | 字数区间  | 判定依据
    -------------+-----------+-----------------------------------------------
    compare      | 750–850   | 对比类：2–5 项深度横评，每项一小段结论即可，
    （兜底档）   |           | 篇幅不需要太长。
    tutorial     | 800–900   | 步骤/流程类：要把操作步骤展开讲，比纯对比略长。
    list         | 950–1100  | 清单类：≥6 条并列推荐，每条都要独立说明（玩法、
    （最宽档）   |           | 适用人群、坑点），篇幅天然更长，卡 750–850 会逼
    |           |           | 撰稿砍内容，反而失真。
    explainer    | 800–900   | 概念解释类：把一个概念讲清楚需要足够篇幅铺陈。

  为何分档：第 1 批改稿时，list 类（free-ai-tools-list）被 750–850 卡住，
  为了不超字数，撰稿被迫把每条推荐压成一句话，丢了「说真话」定位里最该写的
  坑点和适用边界。把 list 抬到 950–1100，等于给这类文章合法篇幅。其余三档的
  区间来自第 1 批实测（compare 均值 ~790、tutorial ~800、explainer ~810），
  上下留 ~50 字余量，既防注水也不逼砍内容。

  article_type 缺失或值非法时：不静默放行，也不硬失败。统一按 compare
  (750–850) 兜底校验，同时打一条 WARN「未声明 article_type，按 compare 档校验」
  （未知值则提示具体值），让编排/撰稿一眼看到该补字段。超上限和低于下限都会报，
  不只卡下限。

输出末尾两列「均句长」「短句%」是 11)/12) 的实测值，便于跨批次追踪基线。
原有九项的列格式未改动。
"""
import re, sys, os

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drafts")

# 已上线 slug：直接扫 drafts/，不再手工维护（每批新增 10 篇无需改本文件）
FILES = sorted(
    f[:-3] for f in os.listdir(HERE) if f.endswith(".md")
) if os.path.isdir(HERE) else []


def _load_planned():
    """从选题总表解析全部 100 个已规划 slug（第 8 列），支撑链接规范 B2 的『预埋』。

    支柱页需要一次性把本簇全部卫星 slug 写进 internal_links，卫星上线后自动
    生效（build_articles.py 对未上线目标会跳过渲染）。这些 slug 当下不在
    drafts/ 里，若按「不存在即 FAIL」处理，支柱页稿子会当场自检失败。
    因此改为三态：已上线 → 过；总表内但未上线 → WARN（预埋）；两者都不在 → FAIL（多半是拼错）。
    """
    root = os.path.dirname(os.path.abspath(__file__))
    import glob
    planned = set()
    for p in glob.glob(os.path.join(root, "research", "brief-learntide-100-*.md")):
        with open(p, encoding="utf-8") as f:
            for line in f:
                cells = [c.strip() for c in line.split("|")]
                # 表格行：| 编号 | 栏目 | 标题 | 主KW | 长尾 | 意图 | 竞争度 | slug | 聚类 | 批次 |
                if len(cells) >= 10 and re.fullmatch(r"\d{3}", cells[1] or ""):
                    s = cells[8]
                    if re.fullmatch(r"[a-z0-9-]+", s or ""):
                        planned.add(s)
    return planned


PLANNED = _load_planned()
BAN = ["神器", "躺平", "颜值飙升", "暴富", "随着人工智能", "众所周知",
       "毋庸置疑", "SWE-bench", "上下文窗口", "待核实", "TODO"]
# 2026-08-06 加「待核实/TODO」：第五批曾残留 [待核实] 占位符，编辑审查建议列入禁词从源头堵住。
# 注意不加「待补充」：ai-reading-notes-method 正文教读者「没有例子就标待补充」属教学内容，会误伤。
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u26FF]")
REQ = ["id", "slug", "title", "category", "primary_keyword", "meta_title",
       "meta_description", "lede", "internal_links", "date", "verified"]
ALLOWED_PATHS = {"../index.html", "../tools.html", "../about.html",
                 "ai-weekly-report-guide.html", "free-ai-image-tools-2026.html",
                 "ai-chat-assistant-compare.html"}

LEDE_ECHO_MAX = 8      # 检查 10：lede 与正文允许的最大连续重合字数
SHORT_SENT_MAX = 12    # 检查 11：多少字以内算短句
SHORT_RATIO_MIN = 15   # 检查 11：短句占比下限（%）
AVG_SENT_MAX = 26      # 检查 12：平均句长上限（字）
DISCLAIMER = re.compile(r"以官网[^。，、；]{0,10}为准")   # 检查 13
NOT_A_BUT_B = re.compile(r"不是[^。；\n]{1,20}?[，,](?:而是|是|不是)")  # 检查 14

# 字数分档（硬失败，但区间随 article_type 变）。依据见脚本头注释「字数分档」一节。
WORD_TIERS = {
    "compare":   (750, 850),
    "tutorial":  (800, 900),
    "list":      (950, 1100),
    "explainer": (800, 900),
}
TIER_DEFAULT = "compare"  # article_type 缺失/非法时兜底，并打 WARN


def norm(x):
    return re.sub(r"[\s\u3000]", "", x).lower()


def width(s):
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


def bare(s):
    """剥掉标点与空格，只留文字，用于 lede 重合比对。"""
    return re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]", "", s)


def longest_common(a, b):
    """返回 a 与 b 的最长连续公共子串（长度, 内容）。"""
    if not a or not b:
        return 0, ""
    prev = [0] * (len(b) + 1)
    best = end = 0
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        ai = a[i - 1]
        for j in range(1, len(b) + 1):
            if ai == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best, end = cur[j], i
        prev = cur
    return best, a[end - best:end]


def prose_sentences(nocode):
    """正文散文句长列表，跳过标题、表格、引用块。

    只要含至少 1 个汉字就算一句。不能用「>2 字才算」来过滤碎片：那会把
    「别用。」这种真短句一起丢掉，而丢掉短句恰好会压低短句占比，等于反向
    惩罚我们想鼓励的写法。切分后的空串和纯标点段本来就是 0 字，天然被排除。
    """
    paras = [p for p in nocode.split("\n\n")
             if p.strip() and not p.strip().startswith(("#", "|", ">", "```"))]
    lens = []
    for p in paras:
        for s in re.split(r"[。！？]", p):
            n = len(re.findall(r"[\u4e00-\u9fff]", s))
            if n > 0:
                lens.append(n)
    return lens


bad = warn_files = 0
print("%-30s %4s %3s %3s %3s %4s %4s %6s %5s  %s"
      % ("slug", "字数", "H2", "码块", "内链", "题宽", "述宽",
         "均句长", "短句%", "状态"))

for s in FILES:
    fp = os.path.join(HERE, s + ".md")
    text = open(fp, encoding="utf-8").read()
    fm, body = text.split("---", 2)[1], text.split("---", 2)[2]
    nocode = re.sub(r"```.*?```", "", body, flags=re.S)
    # 2026-08-10：排除图片语法 `![alt](path)` 的 alt 文本，避免图片 alt 算进正文字数
    nocode = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", nocode)
    cjk = len(re.findall(r"[\u4e00-\u9fff]", nocode))
    h2s = re.findall(r"^## (.+)$", body, flags=re.M)
    code = len(re.findall(r"^```", body, flags=re.M)) // 2
    kw = norm(re.search(r"primary_keyword: (.+)", fm).group(1))
    mt = re.search(r"meta_title: (.+)", fm).group(1).strip()
    md = re.search(r"meta_description: (.+)", fm).group(1).strip()
    lede = re.search(r"lede: (.+)", fm).group(1).strip()
    issues = []
    warns = []

    # ── 字数分档校验（2026-08-04 追加，伟超批）──
    # 读 article_type，按档套区间；缺失/非法 → 按 compare 兜底 + WARN。
    at = re.search(r"^article_type: (.+)$", fm, flags=re.M)
    atype = at.group(1).strip() if at else None
    if atype not in WORD_TIERS:
        if atype is None:
            warns.append("未声明 article_type，按 compare 档校验")
        else:
            warns.append("article_type「%s」未知，按 compare 档校验" % atype)
        atype = TIER_DEFAULT
    lo, hi = WORD_TIERS[atype]
    if cjk < lo:
        issues.append("字数%d（%s 档下限%d）" % (cjk, atype, lo))
    elif cjk > hi:
        issues.append("字数%d（%s 档上限%d）" % (cjk, atype, hi))
    if not 4 <= len(h2s) <= 5:
        issues.append("H2=%d" % len(h2s))
    if code < 1:
        issues.append("无代码块")
    if kw not in norm(nocode.strip())[:130]:
        issues.append("开头无KW")
    if not any(kw in norm(h) for h in h2s):
        issues.append("H2无KW")
    if kw not in norm(nocode.strip().split("\n")[-1]):
        issues.append("结尾无KW")
    miss = [r for r in REQ if not re.search(r"^%s:" % r, fm, flags=re.M)]
    if miss:
        issues.append("缺字段" + ",".join(miss))
    if EMOJI.search(body):
        issues.append("含emoji")
    # 主关键词本身含禁词时放行：禁词是选题总表规划的主题词（如 088「上下文窗口是什么」），
    # 属于合法核心主题而非滥用措辞。2026-08-06 加。
    kw_lower = re.search(r"^primary_keyword:\s*(.+)$", fm, flags=re.M)
    kw_lower = kw_lower.group(1).strip().lower() if kw_lower else ""
    for b in BAN:
        if b.lower() in body.lower() and b.lower() not in kw_lower:
            issues.append("禁词" + b)
    # 正文内链：从「一律禁止」改为「校验目标存在」，保留死链防护
    # 2026-08-10：排除图片语法 `![alt](path)`，避免图片 src 被误判为内链目标
    for _anchor, href in re.findall(r"(?<!!)\[([^]]+)\]\(([^)]+)\)", nocode):
        tgt = href.split("#")[0].split("?")[0].strip()
        if tgt.startswith(("http://", "https://")):
            continue                              # 外链另有规范
        if tgt in ALLOWED_PATHS:
            continue
        if tgt.endswith(".html") and tgt[:-5] in FILES:
            continue
        issues.append("正文内链目标不存在:" + tgt)
    if re.search(r"^# ", body, flags=re.M):
        issues.append("含H1")
    nl = len(re.findall(r"^  - (?:slug|path):", fm, flags=re.M))
    if not 3 <= nl <= 5:
        issues.append("内链%d条" % nl)
    for p in re.findall(r"^    path: (.+)$", fm, flags=re.M) + \
             re.findall(r"^  - path: (.+)$", fm, flags=re.M):
        if p.strip() not in ALLOWED_PATHS:
            issues.append("非法path:" + p.strip())
    for target in re.findall(r"^  - slug: (.+)$", fm, flags=re.M):
        t = target.strip()
        if t in FILES:
            continue
        if t in PLANNED:                      # 规范 B2 预埋：构建器会自动跳过
            warns.append("预埋链接（目标未上线）:" + t)
            continue
        issues.append("内链slug不存在:" + t)
    if not 52 <= width(mt) <= 64:
        issues.append("题宽%d" % width(mt))
    if not 145 <= width(md) <= 162:
        issues.append("述宽%d" % width(md))
    ledec = len(re.findall(r"[\u4e00-\u9fff]", lede))
    if not 30 <= ledec <= 50:
        issues.append("lede %d字" % ledec)
    # 反向提醒必须存在于结尾段
    if "别" not in nocode[-300:] and "不要" not in nocode[-300:]:
        issues.append("无反向提醒")

    # ── 检查 10：lede 与正文连续重合（硬失败）
    echo_n, echo_s = longest_common(bare(lede), bare(nocode))
    if echo_n >= LEDE_ECHO_MAX:
        issues.append("lede重复%d字「%s」" % (echo_n, echo_s))

    # ── 检查 11 / 12：句子节奏（告警）
    lens = prose_sentences(nocode)
    avg = sum(lens) / len(lens) if lens else 0
    ratio = (sum(1 for x in lens if x <= SHORT_SENT_MAX) / len(lens) * 100
             if lens else 0)
    if ratio < SHORT_RATIO_MIN:
        warns.append("短句%.0f%%" % ratio)
    if avg > AVG_SENT_MAX:
        warns.append("均句长%.1f" % avg)

    # ── 检查 13：免责措辞复读（告警）
    for phrase, n in {p: DISCLAIMER.findall(nocode).count(p)
                      for p in DISCLAIMER.findall(nocode)}.items():
        if n > 1:
            warns.append("免责「%s」%d次" % (phrase, n))

    # ── 检查 14：「不是 A，是 B」句式（告警）
    nab = len(NOT_A_BUT_B.findall(nocode))
    if nab > 1:
        warns.append("不是A是B×%d" % nab)

    if issues:
        bad += 1
    if warns:
        warn_files += 1

    status = " | ".join(issues) if issues else ""
    if issues and warns:
        status = "FAIL: " + status + "  ／ WARN: " + " | ".join(warns)
    elif issues:
        status = "FAIL: " + status
    elif warns:
        status = "WARN: " + " | ".join(warns)
    else:
        status = "OK"

    print("%-30s %4d %3d %3d %3d %4d %4d %6.1f %5.0f  %s"
          % (s, cjk, len(h2s), code, nl, width(mt), width(md),
             avg, ratio, status))

print()
print("硬性交付标准：" + ("%d 篇未通过" % bad if bad else "全部 %d 篇通过" % len(FILES)))
print("质量基线告警：" + ("%d 篇有告警（不阻塞交付）" % warn_files if warn_files else "无"))
print()
print("=== 可以交付 ===" if bad == 0 else "=== %d 篇必须修改 ===" % bad)
