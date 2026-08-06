#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心词密度修复：把每篇核心词密度补到 1-1.5%（安全区间）。

流程：
  1. 从 primary_keyword 提取核心词（实体表单趟最长匹配 + 去后缀/描述词 + 方法类拆 AI/名词）
  2. 计算当前核心词密度，与目标（取 1.2% 中点）比，得出需补次数
  3. 在首段后 / 各 H2 前 / 结尾 轮流插入含核心词的自然句子

用法：
  python scripts/keyword_density_fix.py --dry-run          # 仅看核心词提取与缺口
  python scripts/keyword_density_fix.py --apply            # 全量修复
  python scripts/keyword_density_fix.py --apply --limit 5  # 试点 5 篇
"""
import os
import re
import sys

DRAFTS_DIR = os.path.join(os.path.dirname(__file__), "..", "drafts")
CJK = re.compile(r"[\u4e00-\u9fff]")

# 实体标准化表（key 小写或中文，value 标准写法）。
# 注意：含多字符实体（通义千问 / 文心一言 / 通义灵码 等）必须作为独立 key，
# 以便下面用「按长度降序」的单趟 regex 替换，避免「通义」先命中再把结果二次命中。
CORE_ENTITIES = {
    "deepseek": "DeepSeek", "深度求索": "DeepSeek",
    "chatgpt": "ChatGPT", "openai": "OpenAI", "anthropic": "Anthropic",
    "claude": "Claude", "kimi": "Kimi", "moonshot": "Kimi",
    "doubao": "豆包", "豆包": "豆包", "字节跳动": "字节", "字节": "字节",
    "qwen": "Qwen", "通义千问": "通义千问", "通义灵码": "通义灵码", "通义": "通义千问",
    "gemini": "Gemini", "google": "Google",
    "midjourney": "Midjourney", "mj": "Midjourney",
    "stable diffusion": "Stable Diffusion", "sd": "Stable Diffusion",
    "dall": "DALL·E", "runway": "Runway",
    "kling": "Kling", "可灵": "可灵",
    "jimeng": "即梦", "sora": "Sora",
    "suno": "Suno", "udio": "Udio",
    "elevenlabs": "ElevenLabs", "notebooklm": "NotebookLM",
    "notion": "Notion", "perplexity": "Perplexity",
    "cursor": "Cursor", "copilot": "Copilot", "github": "GitHub",
    "grammarly": "Grammarly", "jianying": "剪映", "heygen": "HeyGen",
    "zhipu": "智谱清言", "智谱清言": "智谱清言", "清言": "智谱清言",
    "wenxin": "文心一言", "文心一言": "文心一言", "文心": "文心一言",
    "huoshan": "火山", "miota": "秘塔", "lingma": "通义灵码", "qoder": "Qoder",
    "token": "token", "rag": "RAG", "llm": "大模型",
}
# 单趟最长匹配替换（先按 key 长度降序，避免子串二次命中）
_ENTITY_ITEMS = sorted(CORE_ENTITIES.items(), key=lambda kv: -len(kv[0]))
_ENTITY_RE = re.compile("|".join(re.escape(k) for k, _ in _ENTITY_ITEMS))
def _entity_repl(m):
    return CORE_ENTITIES[m.group(0)]

# 词尾/描述性后缀，命中即剥除（正则为「整体末尾」）
SUFFIX = re.compile(
    r"(哪个好|好用吗|值得\S*?吗|怎么写|怎么做|怎么用|怎么样|是什么|推荐|对比|"
    r"技巧|教程|指南|方法|如何|攻略|评测|值得买吗|值得开吗|值得订阅吗|"
    r"怎么学|怎么练|怎么选|盘点|横评|清单|完全指南|测评|排行|排名|合集|"
    r"汇总|总结|介绍|入门|进阶|实战|案例|模板|素材|资源|集合|列表|"
    r"大全|网站|平台|软件|工具|区别|是什么|好用不|好不好用)$"
)
# 英文品牌修饰词（plus / pro / free ...），作为独立 token 剥除
BRAND_MODS = re.compile(
    r"\b(plus|pro|free|max|mini|lite|standard|premium|api|web|app|online)\b",
    re.IGNORECASE,
)
# 描述性中文名词（替代品 / 排行 等），整段（尤其末尾）剥除，避免成为核心词
DESC_TERMS = sorted(
    ["国内替代品", "替代品", "国内版", "国际版", "免费版", "收费版", "手机版",
     "网页版", "电脑版", "中文版", "排行", "排名", "榜单", "合集", "清单",
     "推荐", "指南", "教程", "攻略", "方法", "技巧", "工具", "软件", "平台",
     "网站", "大全", "汇总", "总结", "介绍", "入门", "进阶", "实战", "案例",
     "模板", "素材", "资源", "集合", "列表", "测评", "评测", "对比", "区别",
     "是什么", "怎么样", "好用吗", "好用不", "怎么用", "怎么写", "怎么做",
     "怎么学", "怎么练", "怎么选", "哪个好用", "哪个好", "新手", "零基础",
     "小白", "免费", "基础版", "基础", "完整版", "够用吗", "能用吗",
     "值得吗", "划得来吗", "配音", "配音工具"],
    key=len, reverse=True,
)
DESC_RE = re.compile("(" + "|".join(DESC_TERMS) + ")")
# 疑问词：命中的残留视为「问题短语」而非名词，丢弃
INTERROG = re.compile(r"怎么|如何|怎样|啥|什么|为什么|为何|哪|吗|呢|咋|办不")
# 独立「ai」token：不被 ASCII 字母包围（Python \b 是 Unicode 感知的，CJK 也算 \w，
# 故 ai+中文 之间无边界，必须用字母 lookaround 避免把 email/training 误判）
AI_RE = re.compile(r"(?<![a-z])ai(?![a-z])", re.IGNORECASE)
VERBS = ["写", "做", "整理", "辅助", "处理", "生成", "优化", "练习", "模拟",
         "学", "练", "选", "拍", "投喂", "润色", "翻译", "总结", "梳理",
         "规划", "设计", "给"]


def parse(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        return None, text
    return m.group(1), m.group(2)  # fm, body


def get_pk(fm):
    for line in fm.split("\n"):
        if line.startswith("primary_keyword:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return ""


def strip_md(body):
    txt = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    txt = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", txt)
    txt = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", txt)
    txt = re.sub(r"[#>*>`\-\[\]()!|:]", " ", txt)
    return txt


def _clean_part(p):
    """处理 SPLIT 切出的单个片段，返回核心词列表（可能 0~2 个）。"""
    p = SUFFIX.sub("", p).strip()
    p = BRAND_MODS.sub("", p).strip()
    if not p:
        return []
    p = _ENTITY_RE.sub(_entity_repl, p)  # 单趟最长匹配替换
    p = DESC_RE.sub("", p).strip()       # 剥描述性名词
    if not p:
        return []
    # AI 拆分：仅当独立 token（不被 ASCII 字母包围）
    if AI_RE.search(p):
        rest = AI_RE.sub("", p).strip()
        for vb in VERBS:
            rest = rest.replace(vb, "").strip()
        has_cjk = bool(CJK.search(rest))
        is_clean = bool(rest) and has_cjk and not INTERROG.search(rest)
        if is_clean:
            return ["AI", rest]
        return ["AI"]
    if p:
        return [p]
    return []


def extract_core_terms(pk):
    if not pk:
        return []
    low = pk.lower()
    parts = re.split(r"\s*(?:和|与|vs|对比| versus |/|、)\s*", low, flags=re.IGNORECASE)
    terms = []
    for p in parts:
        terms.extend(_clean_part(p))
    seen, out = set(), []
    for t in terms:
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def core_density(terms, body):
    txt = strip_md(body)
    n = len(CJK.findall(txt))
    if n == 0 or not terms:
        return 0, 0, 0.0
    low_txt = txt.lower()
    total = sum(low_txt.count(t.lower()) for t in terms)
    return total, n, total / n * 100


def build_sentences(terms, need):
    """生成 need 个含核心词的自然句子（每句含 1 次核心词）。"""
    if len(terms) >= 2:
        a, b = terms[0], terms[1]
        pool = [
            f"{a}和{b}常被放在一起比，但其实关注点不同。",
            f"选{a}还是{b}，看你手上的活落在哪一边。",
            f"{a}的优势在一处，{b}的优势在另一处，别混为一谈。",
            f"回头看，{a}和{b}没有绝对好坏，只有合不合适。",
        ]
    else:
        t = terms[0] if terms else "它"
        pool = [
            f"聊到{t}，先要明确它解决的是哪类问题。",
            f"理解{t}的关键，是看它替你省下了什么。",
            f"关于{t}，不少人一开始会踩坑，下面说怎么避。",
            f"说到底，{t}只是工具，用得对才值。",
        ]
    if need <= len(pool):
        return pool[:need]
    return (pool * (need // len(pool) + 1))[:need]


def insert_sentences(body, sentences):
    if not sentences:
        return body
    parts = body.split("\n## ")
    out = [parts[0]]
    si = 0
    if si < len(sentences):
        out[0] = out[0] + "\n\n" + sentences[si]
        si += 1
    for i in range(1, len(parts)):
        seg = "## " + parts[i]
        if si < len(sentences):
            seg = sentences[si] + "\n\n" + seg
            si += 1
        out.append(seg)
    while si < len(sentences):
        out.append(sentences[si])
        si += 1
    return "\n".join(out)


def process_file(slug, apply=False):
    path = os.path.join(DRAFTS_DIR, slug + ".md")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    fm, body = parse(text)
    if fm is None:
        return None
    pk = get_pk(fm)
    terms = extract_core_terms(pk)
    if not terms:
        return {"slug": slug, "terms": [], "density": 0.0, "need": 0, "skipped": True}
    cnt, n, d = core_density(terms, body)
    target = max(1, round(n * 0.012))
    need = max(0, target - cnt)
    if need == 0:
        return {"slug": slug, "terms": terms, "density": d, "need": 0, "skipped": True}
    sentences = build_sentences(terms, need)
    if apply:
        new_body = insert_sentences(body, sentences)
        new_text = "---\n" + fm + "\n---\n" + new_body  # 保留完整 front matter
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
    return {"slug": slug, "terms": terms, "density": d, "need": need,
            "sentences": sentences if apply else None}


def main():
    apply = "--apply" in sys.argv
    limit = None
    for a in sys.argv[1:]:
        if a.startswith("--limit"):
            limit = int(a.split("=")[1]) if "=" in a else int(sys.argv[sys.argv.index(a) + 1])
    slugs = [f[:-3] for f in sorted(os.listdir(DRAFTS_DIR)) if f.endswith(".md")]
    done = 0
    for slug in slugs:
        r = process_file(slug, apply=apply)
        if r is None or r.get("skipped"):
            continue
        done += 1
        if not apply:
            print(f"{slug:36} 核心词={r['terms']} 密度={r['density']:.2f}% 需补={r['need']}")
        else:
            print(f"[+] {slug:36} 核心词={r['terms']} 插入 {r['need']} 句")
        if limit and done >= limit:
            break
    print(f"\n=== {'已写入' if apply else '预览'} {done} 篇（密度达标篇跳过）===")


if __name__ == "__main__":
    main()
