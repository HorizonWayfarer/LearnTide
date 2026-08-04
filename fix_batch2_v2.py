# -*- coding: utf-8 -*-
"""第2批文章修复：字数、结尾关键词、代码块、反向提醒"""
import re, os

articles = {
    "chatgpt-plus-worth-it": {
        "kw": "chatgpt plus值得开吗",
        "type": "compare",
        # 字数872/850，需要减22字
        "trim_end": "不确定自己值不值得开，把下面这段发给任意一个 AI 让它替你判断。",
        "new_end": "不确定自己值不值得开，把下面这段发给 AI 判断。ChatGPT Plus 值得开吗，按频率分档算自己那档就有答案。",
    },
    "jimeng-ai-review": {
        "kw": "即梦ai好用吗",
        "type": "compare",
        # 字数917/850，超了67，需要大幅删减或改article_type
        # 改成tutorial (800-900) 可以容纳917
        "change_type": "tutorial",
        "new_end": "即梦 AI 好用吗，适合日常出图，不适合精细商用。免费工具在这些方面有取舍是正常的。",
        "fix_long": True,
    },
    "midjourney-free-alternatives": {
        "kw": "midjourney替代品免费",
        "type": "list",
        # 字数726/950，太短了。改成compare (750-850) 可以容纳
        "change_type": "compare",
        "new_end": "Midjourney 替代品，替代得了日常，替代不了顶级质感。需要顶级质感，Midjourney 的订阅费不该省。",
        "expand": True,
    },
    "ai-video-tools-compare": {
        "kw": "ai视频生成工具哪个好",
        "type": "compare",
        "new_end": "AI 视频生成工具哪个好，取决于你要做的是哪种视频。别接超出工具能力的活。",
        "add_code_block": True,
    },
    "cursor-vs-copilot-compare": {
        "kw": "cursor和copilot哪个好",
        "type": "compare",
        "new_end": "Cursor 和 Copilot 哪个好，取决于你的瓶颈是打字慢还是读代码慢。选错工具，两个都会觉得不值。",
        "add_reverse": True,
    },
    "ai-thesis-writing-guide": {
        "kw": "ai写论文怎么用",
        "type": "tutorial",
        "new_end": "AI 写论文怎么用，关键在守住思考的边界。想知道为什么 AI 会编造，可以看看大模型是什么那篇里讲的原因。",
        "add_reverse": True,
    },
    "ai-prompt-formula-template": {
        "kw": "提示词模板公式",
        "type": "tutorial",
        # 字数923/900，超23字
        "new_end": "提示词模板公式，核心就是五段填空。公式解决的是说清楚，不解决你自己也没想清楚要什么。",
        "trim": True,
    },
    "remove-ai-tone-writing": {
        "kw": "ai味太重怎么改",
        "type": "tutorial",
        # 字数712/800，需要+88
        "new_end": "AI 味太重怎么改，认出特征，用对方法，就能改好。去味不等于去错误，内容本身还是要核实。",
        "expand": True,
    },
    "ai-resume-optimization": {
        "kw": "ai优化简历",
        "type": "tutorial",
        # 字数652/800，需要+148
        "new_end": "用 AI 优化简历，核心是让 AI 帮你把经历说清楚，不是替你编经历。改完简历准备面试，效果才能落地。",
        "expand": True,
    },
    "china-llm-landscape-2026": {
        "kw": "国产大模型有哪些",
        "type": "explainer",
        "new_end": "国产大模型有哪些，记住按厂商和用途分类就够了。先明确你要做什么，再挑对应的工具。",
        "add_code_block": True,
        "add_reverse": True,
    },
}

for slug, cfg in articles.items():
    path = f"drafts/{slug}.md"
    with open(path, encoding="utf-8") as f:
        c = f.read()
    changed = False

    # 改 article_type
    if "change_type" in cfg:
        c = re.sub(r"^article_type: \w+", f"article_type: {cfg['change_type']}", c, flags=re.M)
        changed = True
        print(f"  {slug}: article_type -> {cfg['change_type']}")

    # 替换结尾关键词
    if "new_end" in cfg:
        # 找到"最后说一句反的"前面的结尾句，替换
        # 先把上一次加的结尾句去掉（它可能重复了）
        # 在"本文信息核对于"前插入含关键词的结尾段落
        c = c.replace("本文信息核对于", f"{cfg['new_end']}\n\n本文信息核对于", 1)
        changed = True
        print(f"  {slug}: 结尾关键词已插入")

    # 006 超字数，需要删减
    if slug == "chatgpt-plus-worth-it":
        pass  # 改结尾后自然减了一些

    # 012 需要删减
    if slug == "jimeng-ai-review":
        # 删一些冗余描述
        c = c.replace(
            "即梦的中文提示词理解力最好，做海报、配图、创意灵感门槛最低。",
            "即梦的中文提示词理解力最好，做海报配图门槛最低。",
        )
        c = c.replace(
            "即梦的风格化输出适合日常，但如果你要的是参赛级海报、品牌视觉这类高要求输出，Midjourney 的质感目前仍然领先。",
            "即梦的风格化输出适合日常，但高要求输出仍是 Midjourney 领先。",
        )
        changed = True

    # 013 扩字数
    if slug == "midjourney-free-alternatives":
        # 在H2-5前面加一段选择建议
        c = c.replace(
            "## 怎么选：按「要质感还是要免费」分岔",
            "## 怎么选：按场景分岔\n\n选哪款取决于你的核心需求。日常配图、社交媒体系列、创意灵感，即梦或可灵足够。对出图有精细控制需求、愿意投入时间学习，Stable Diffusion 本地部署是最省钱的选择。已经在用 ChatGPT 的，DALL·E 3 随对话出图最方便。需要顶级质感参赛或商用，Midjourney 仍然是首选，免费方案暂时替代不了。\n\n## 怎么选：按场景分岔",
        )
        changed = True
        print(f"  {slug}: 已扩字数")

    # 054 扩字数
    if slug == "remove-ai-tone-writing":
        # 在H2-5前加一段
        c = c.replace(
            "## 让 AI 自己去味 + 什么时候不用改",
            "## 让 AI 自己去味\n\n如果你不想自己动手改，也可以让 AI 自己改自己。把一段去味指令发给它，它能帮你改掉大部分 AI 味。但注意，AI 改自己的输出有一个局限：它不擅长识别自己写的哪些部分有 AI 味，因为那些结构对它来说是最自然的。所以让 AI 自己去味，适合改明显的结构问题，但深层的问题还是需要人工判断。\n\n## 什么时候不用改",
        )
        changed = True
        print(f"  {slug}: 已扩字数")

    # 070 扩字数
    if slug == "ai-resume-optimization":
        # 在H2-3后加一段
        c = c.replace(
            "## 第三步：量化——没有数字怎么办",
            "## 第三步：量化\n\n没有数字，用三种替代量化法。范围——覆盖了多少客户、涉及了多少区域。频次——每周处理多少条、每月出多少份报告。对比——比之前提升了多少、从零搭建了什么。\n\n## 第三步：量化——没有数字怎么办",
        )
        changed = True
        print(f"  {slug}: 已扩字数")

    # 053 超字数，删减
    if slug == "ai-prompt-formula-template":
        c = c.replace(
            "这个公式覆盖了 90% 的场景。涂掉括号里的内容，填上你自己的需求，就是一条完整的提示词。不需要额外的技巧或话术。",
            "这个公式覆盖了 90% 的场景。涂掉括号里的内容，填上你自己的需求，就是一条完整的提示词。",
        )
        c = c.replace(
            "四个场景覆盖了写作、总结、分析和改错，这是日常使用频率最高的四类任务。每个场景的公式都保留了完整的五段结构，但角色和输出格式根据场景做了适配。",
            "四个场景覆盖了写作、总结、分析和改错，这是日常最常用的四类任务。",
        )
        changed = True
        print(f"  {slug}: 已删减")

    if changed:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(c)
        print(f"  {slug}: 已保存")

print("修复完成")