# -*- coding: utf-8 -*-
"""最终修复2：lede重复、字数、题宽、反向提醒"""
import re, os

fixes = {
    "chatgpt-plus-worth-it": {
        # 字数859/850，lede重复
        "lede": "ChatGPT Plus 值得开吗，没有统一答案，先看自己一周用几次。",
        "trim": [
            ("高频用户还有一个隐藏成本：免费版的消息上限和降级会让你在关键时刻停下来等，中断工作流。这个中断的代价比月费更大。", "高频用户还有一个隐藏成本：免费版上限和降级会中断工作流，代价比月费更大。"),
        ],
    },
    "jimeng-ai-review": {
        # 字数921/900，无代码块
        "lede": "即梦 AI 是字节出品的免费中文出图工具，中文提示词不用翻译，国内直接可用。",
        "trim": [
            ("即梦的中文提示词理解力最好，做海报配图门槛最低。下面是一个中文提示词结构模板：", "即梦的中文提示词理解力最好。下面是一个提示词结构模板："),
        ],
    },
    "midjourney-free-alternatives": {
        # 字数870/850，结尾无KW，lede重复
        "lede": "Midjourney 要付费还要用 Discord，免费替代品到底能不能顶？",
        "trim": [
            ("Midjourney 替代品，替代得了日常，替代不了顶级质感。", "免费替代品，替代得了日常，替代不了顶级质感。"),
        ],
    },
    "ai-video-tools-compare": {
        # 字数875/850，题宽51，lede重复
        "lede": "搜 AI 视频工具会搜到一堆名字，但它们在做三件完全不同的事。",
        "trim": [
            ("## AI 视频生成工具哪个好？先分清三类再选\n\nAI 视频生成工具这个说法底下的东西差别很大，", "## AI 视频生成工具哪个好？先分清三类再选\n\n"),
        ],
    },
    "cursor-vs-copilot-compare": {
        # 无反向提醒
        "reverse": True,
    },
    "ai-prompt-formula-template": {
        # lede重复
        "lede": "提示词模板公式就五个空：角色、任务、背景、格式、约束。填完就是一条好指令。",
    },
    "remove-ai-tone-writing": {
        # 题宽47，lede 24字
        "lede": "AI 味不是玄学，它有四个特征。认出来，改起来就快。",
    },
    "ai-resume-optimization": {
        # 字数777/800，lede重复
        "lede": "简历没回音，不是经历不够，是只写了做什么没写做成了什么。",
        "expand": "改完简历，再花同样时间准备自我介绍和面试话术，把纸面上的亮点变成可说出来的内容。"
    },
    "china-llm-landscape-2026": {
        # 字数905/900，lede重复
        "lede": "国产大模型名字听过一堆但分不清谁是谁家的？一张表看懂。",
        "trim": [
            ("先用一张表看清主要玩家，再按类型展开。\n\n```\n通用对话型：豆包、Kimi、通义千问、文心一言、智谱清言\n推理开源型：DeepSeek、通义系列\n多模态生成型：即梦（图像）、可灵（视频）、混元（综合）\n```\n\n| 厂商 | 模型 | 代表产品 | 类型 |", "| 厂商 | 模型 | 代表产品 | 类型 |"),
        ],
    },
}

for slug, cfg in fixes.items():
    path = f"drafts/{slug}.md"
    with open(path, encoding="utf-8") as f:
        c = f.read()
    changed = False

    if "lede" in cfg:
        c = re.sub(r"^lede: .+$", "lede: " + cfg["lede"], c, flags=re.M)
        changed = True
        print(f"  {slug}: lede 已修复")

    if "trim" in cfg:
        for old, new in cfg["trim"]:
            if old in c:
                c = c.replace(old, new, 1)
                changed = True
                print(f"  {slug}: 已删减")

    if "reverse" in cfg:
        if "别" not in c[-300:] and "不要" not in c[-300:]:
            c = c.replace("最后说一句反的：", "最后说一句反的：**别让 AI 替你做决定，**", 1)
            changed = True
            print(f"  {slug}: 反向提醒已修复")

    if "expand" in cfg:
        c = c.replace("最后说一句反的：", cfg["expand"] + "\n\n最后说一句反的：", 1)
        changed = True
        print(f"  {slug}: 已扩字数")

    # 054 题宽修复
    if slug == "remove-ai-tone-writing":
        c = c.replace("meta_title: AI 味太重怎么改？去掉AI味的六个技巧 — Learntide", "meta_title: AI 味太重怎么改？六个去AI味技巧和方法 — Learntide")
        changed = True

    if changed:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(c)
        print(f"  {slug}: 已保存")

print("修复完成")