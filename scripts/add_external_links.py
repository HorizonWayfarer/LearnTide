#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 Learntide 草稿批量补充官方外链。

扫描 drafts/<slug>.md，在正文中为首次出现的核心 AI 工具/平台名称
添加官方链接，语法与项目现有外链一致：[名称](url){:target="_blank"}

规则：
- 跳过 front matter（第一个 --- 到第二个 --- 之间）
- 跳过代码块（```...```，先抽走保护，处理完还原）
- 跳过已被 markdown 链接包裹的词
- 每个工具名全文只加一次（占位符防嵌套/跨段重复）
- 每篇最多补 3 条不同工具外链
- 按工具重要性排序，优先补最核心的大模型/平台

用法：
    python scripts/add_external_links.py --dry-run    # 只打印，不修改
    python scripts/add_external_links.py --apply       # 实际写入
"""

import os
import re
import sys

DRAFTS_DIR = os.path.join(os.path.dirname(__file__), "..", "drafts")

# 工具映射：名称 -> 官方 URL
# 顺序即优先级（核心大模型/平台在前，按长度降序避免子串误伤）
TOOLS = [
    # 大模型 / 对话
    ("GitHub Copilot", "https://github.com/features/copilot"),
    ("ChatGPT", "https://chat.openai.com"),
    ("Claude", "https://claude.ai"),
    ("OpenAI", "https://openai.com"),
    ("Anthropic", "https://www.anthropic.com"),
    ("Gemini", "https://gemini.google.com"),
    ("Google", "https://www.google.com"),
    ("DeepSeek", "https://www.deepseek.com"),
    ("深度求索", "https://www.deepseek.com"),
    ("通义千问", "https://tongyi.aliyun.com"),
    ("通义", "https://tongyi.aliyun.com"),
    ("Qwen", "https://www.qwen.ai"),
    ("Kimi", "https://kimi.moonshot.cn"),
    ("月之暗面", "https://www.moonshot.cn"),
    ("豆包", "https://doubao.com"),
    ("文心一言", "https://yiyan.baidu.com"),
    ("文心", "https://yiyan.baidu.com"),
    ("百度文心", "https://yiyan.baidu.com"),
    ("百度", "https://www.baidu.com"),
    ("智谱清言", "https://www.zhipuai.cn"),
    ("智谱", "https://www.zhipuai.cn"),
    ("讯飞星火", "https://xinghuo.xfyun.cn"),
    ("百川", "https://www.baichuan-ai.com"),
    ("MiniMax", "https://www.minimax.io"),
    ("零一万物", "https://www.01.ai"),
    ("阶跃星辰", "https://www.stepfun.com"),
    ("StepFun", "https://www.stepfun.com"),
    ("混元", "https://hunyuan.tencent.com"),
    ("腾讯", "https://www.tencent.com"),
    ("阿里", "https://www.alibaba.com"),
    ("字节跳动", "https://www.bytedance.com"),
    ("字节", "https://www.bytedance.com"),
    ("Perplexity", "https://www.perplexity.ai"),
    ("秘塔 AI", "https://metaso.cn"),
    ("秘塔", "https://metaso.cn"),
    ("Mistral", "https://mistral.ai"),
    ("Meta", "https://about.meta.com"),
    ("Llama", "https://www.llama.com"),
    ("Microsoft", "https://www.microsoft.com"),
    ("微软", "https://www.microsoft.com"),
    # 编码
    ("Cursor", "https://www.cursor.com"),
    ("GitHub", "https://github.com"),
    ("VS Code", "https://code.visualstudio.com"),
    ("Visual Studio Code", "https://code.visualstudio.com"),
    ("Replit", "https://replit.com"),
    # 图像
    ("Midjourney", "https://www.midjourney.com"),
    ("Stable Diffusion", "https://stability.ai"),
    ("DALL-E", "https://openai.com/dall-e"),
    ("DALL·E", "https://openai.com/dall-e"),
    ("即梦", "https://jimeng.jianying.com"),
    ("Jimeng", "https://jimeng.jianying.com"),
    ("可灵", "https://kling.kuaishou.com"),
    ("Kling", "https://kling.kuaishou.com"),
    ("Runway", "https://runwayml.com"),
    ("快手", "https://www.kuaishou.com"),
    ("Adobe Photoshop", "https://www.adobe.com/products/photoshop.html"),
    ("Photoshop", "https://www.adobe.com/products/photoshop.html"),
    ("Adobe", "https://www.adobe.com"),
    ("Canva", "https://www.canva.com"),
    ("Figma", "https://www.figma.com"),
    # 音频 / 视频
    ("Suno", "https://suno.com"),
    ("Udio", "https://udio.com"),
    ("ElevenLabs", "https://elevenlabs.io"),
    # 办公 / 效率 / 社区
    ("Notion", "https://www.notion.so"),
    ("NotebookLM", "https://notebooklm.google.com"),
    ("飞书", "https://www.feishu.cn"),
    ("钉钉", "https://www.dingtalk.com"),
    ("腾讯会议", "https://meeting.tencent.com"),
    ("微信", "https://weixin.qq.com"),
    ("小红书", "https://www.xiaohongshu.com"),
    ("知乎", "https://www.zhihu.com"),
    ("抖音", "https://www.douyin.com"),
    ("哔哩哔哩", "https://www.bilibili.com"),
    ("B站", "https://www.bilibili.com"),
    ("WPS", "https://www.wps.cn"),
    ("PowerPoint", "https://www.microsoft.com/powerpoint"),
    ("PPT", "https://www.microsoft.com/powerpoint"),
    ("Word", "https://www.microsoft.com/word"),
    ("Excel", "https://www.microsoft.com/excel"),
    ("Office", "https://www.office.com"),
    ("Grammarly", "https://www.grammarly.com"),
    ("Jasper", "https://www.jasper.ai"),
    ("Copy.ai", "https://www.copy.ai"),
    ("Zapier", "https://zapier.com"),
    ("Hugging Face", "https://huggingface.co"),
    ("Descript", "https://www.descript.com"),
]

MAX_LINKS_PER_FILE = 3

# 按名称长度降序，避免子串误伤（如 GitHub Copilot 先于 Copilot）
TOOLS.sort(key=lambda x: -len(x[0]))


def split_front_matter(text):
    """分离 front matter 与正文。"""
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if m:
        return m.group(1), m.group(2)
    return None, text


def process_body(body):
    """
    在正文里为首次出现的工具名加官方链接。
    返回 (new_body, added_list)
    """
    # 1. 抽走代码块，用占位符保护
    code_blocks = re.findall(r"```.*?```", body, flags=re.DOTALL)
    cb_ph = []
    for i, cb in enumerate(code_blocks):
        ph = f"\x02CB{i}\x02"
        cb_ph.append((ph, cb))
        body = body.replace(cb, ph, 1)

    # 1.5 抽走标题行（# 开头），避免标题内嵌链接打断阅读
    heads = list(re.finditer(r"^#{1,6}\s.*$", body, flags=re.MULTILINE))
    for idx, m in enumerate(reversed(heads)):
        ph = f"\x03H{idx}\x03"
        body = body[: m.start()] + ph + body[m.end() :]
    restore_heads = [
        (f"\x03H{idx}\x03", heads[len(heads) - 1 - idx].group(0))
        for idx in range(len(heads))
    ]

    # 2. 在剩余文本中，每个工具名只加一次（占位符防嵌套/跨段重复）
    budget = MAX_LINKS_PER_FILE
    added = []  # (name, url, link_placeholder)
    for name, url in TOOLS:
        if budget <= 0:
            break
        pat = re.compile(
            r"(?<![\[A-Za-z])" + re.escape(name) + r"(?![A-Za-z])",
            re.IGNORECASE,
        )
        m = pat.search(body)
        if not m:
            continue
        link_ph = f"\x01L{len(added)}\x01"
        body = body[: m.start()] + link_ph + body[m.end() :]
        added.append((name, url, link_ph))
        budget -= 1

    # 3. 还原链接占位符为真实 markdown 链接
    for name, url, link_ph in added:
        body = body.replace(link_ph, f"[{name}]({url}){{:target=\"_blank\"}}")

    # 4. 还原代码块
    for ph, cb in cb_ph:
        body = body.replace(ph, cb)

    # 5. 还原标题行
    for ph, h in restore_heads:
        body = body.replace(ph, h)

    return body, [(n, u) for n, u, _ in added]


def process_file(slug, apply=False):
    path = os.path.join(DRAFTS_DIR, slug + ".md")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    fm, body = split_front_matter(text)
    new_body, added = process_body(body)
    if not added:
        return []
    if fm is not None:
        new_text = "---\n" + fm + "\n---\n" + new_body
    else:
        new_text = new_body
    if apply:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
    return added


def main():
    apply = "--apply" in sys.argv
    dry = "--dry-run" in sys.argv or not apply

    # 从 stdin 读取 slug 列表（每行一个），或命令行参数
    slugs = []
    if not sys.stdin.isatty():
        slugs = [l.strip() for l in sys.stdin if l.strip()]
    slugs += [a for a in sys.argv[1:] if not a.startswith("--")]

    total = 0
    for slug in slugs:
        added = process_file(slug, apply=apply)
        if added is None:
            print(f"[SKIP] {slug}  (草稿不存在)")
            continue
        if not added:
            print(f"[ - ] {slug}  (未匹配到工具，跳过)")
            continue
        total += 1
        links = ", ".join(f"{n}→{u}" for n, u in added)
        print(f"[{'+' if apply else '~'}] {slug}: {links}")
    print(f"\n=== {'已写入' if apply else '预览'} {total} 篇，共 {MAX_LINKS_PER_FILE} 条/篇上限 ===")


if __name__ == "__main__":
    main()
