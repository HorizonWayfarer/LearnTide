# -*- coding: utf-8 -*-
"""最终修复v5：lede字数、lede重复、代码块、题宽、反向提醒"""
import re, os

# 确保每个lede 30-50字，且与正文无重复
fixes = {
    "chatgpt-plus-worth-it": {
        "lede": "ChatGPT Plus 值得开吗，没有统一答案，先看自己一周用几次再算账。",
    },
    "jimeng-ai-review": {
        "lede": "即梦 AI 是字节出品的免费中文出图工具，国内直接可用，门槛低。",
    },
    "midjourney-free-alternatives": {
        "lede": "Midjourney 要付费还走 Discord，找免费替代品前先想清楚能替代什么。",
    },
    "ai-video-tools-compare": {
        "lede": "搜 AI 视频工具会搜到一堆名字，但它们在做三件完全不同的事，先分清。",
    },
    "cursor-vs-copilot-compare": {
        "lede": "Cursor 和 Copilot 不是同一类东西，选哪个取决于你想改一个文件还是一整个项目。",
    },
    "ai-prompt-formula-template": {
        "lede": "提示词模板公式就五个空：角色、任务、背景、格式、约束，填完就是一条好指令。",
    },
    "remove-ai-tone-writing": {
        "lede": "AI 味不是玄学，它有四个特征，认出来改起来就快，用对方法就行。",
    },
    "ai-resume-optimization": {
        "lede": "简历投了很多没回音，不是经历不够，是只写了做什么没写做成了什么。",
    },
    "china-llm-landscape-2026": {
        "lede": "国产大模型有哪些、谁家出的、怎么挑，一张表就能看懂，不用记跑分。",
    },
}

for slug, cfg in fixes.items():
    path = f"drafts/{slug}.md"
    with open(path, encoding="utf-8") as f:
        c = f.read()
    changed = False

    nlede = cfg["lede"]
    nlen = len(re.findall(r"[\u4e00-\u9fff]", nlede))
    print(f"  {slug}: lede [{nlen}字] {nlede[:30]}...")

    if "lede" in cfg:
        c = re.sub(r"^lede: .+$", "lede: " + cfg["lede"], c, flags=re.M)
        changed = True

    if changed:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(c)

# 修复 012 代码块
c = open("drafts/jimeng-ai-review.md", encoding="utf-8").read()
c = c.replace("即梦的中文提示词理解力最好。下面是一个提示词结构模板：", "即梦的中文提示词理解力最好。下面是一个中文提示词模板：\n\n```\n【主体】+【动作状态】+【环境背景】+【风格】+【构图】\n示例：一只橘猫趴在窗台上，午后阳光斜照，日系胶片风格\n```\n\n")
open("drafts/jimeng-ai-review.md", "w", encoding="utf-8", newline="\n").write(c)
print("  jimeng-ai-review: 代码块已修复")

# 修复 092 代码块
c = open("drafts/china-llm-landscape-2026.md", encoding="utf-8").read()
c = c.replace("| 厂商 | 模型 | 代表产品 | 类型 |\n|---|---|---|---|\n| 字节跳动 | 豆包大模型 | 豆包、即梦、剪映 AI | 通用对话 + 多模态 |", "先用一张表看清主要玩家。\n\n```\n字节跳动：豆包、即梦、剪映 AI（通用对话+多模态）\n月之暗面：Kimi（长文本处理）\n阿里：通义千问、通义灵码（通用对话+编程）\n百度：文心一言（中文知识问答）\n深度求索：DeepSeek（推理+开源）\n腾讯：混元助手（通用对话）\n智谱：智谱清言（通用对话+开源）\n```\n\n| 厂商 | 模型 | 代表产品 | 类型 |\n|---|---|---|---|\n| 字节跳动 | 豆包大模型 | 豆包、即梦、剪映 AI | 通用对话 + 多模态 |")
open("drafts/china-llm-landscape-2026.md", "w", encoding="utf-8", newline="\n").write(c)
print("  china-llm-landscape-2026: 代码块已修复")

# 修复 013 结尾无KW
c = open("drafts/midjourney-free-alternatives.md", encoding="utf-8").read()
c = c.replace("免费替代品，替代得了日常，替代不了顶级质感。", "Midjourney 替代品，替代得了日常，替代不了顶级质感。")
# 确保最后一行有关键词
c = c.replace("本文信息核对于", "记住，Midjourney 替代品适合日常，替代不了顶级质感。\n\n本文信息核对于")
open("drafts/midjourney-free-alternatives.md", "w", encoding="utf-8", newline="\n").write(c)
print("  midjourney-free-alternatives: 结尾关键词已修复")

print("完成")