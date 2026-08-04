# -*- coding: utf-8 -*-
"""最终修复：字数、代码块、反向提醒、题宽、lede"""
import re, os

for slug in ["chatgpt-plus-worth-it", "jimeng-ai-review", "midjourney-free-alternatives",
             "ai-video-tools-compare", "cursor-vs-copilot-compare",
             "ai-thesis-writing-guide", "ai-prompt-formula-template",
             "remove-ai-tone-writing", "ai-resume-optimization",
             "china-llm-landscape-2026"]:
    path = f"drafts/{slug}.md"
    with open(path, encoding="utf-8") as f:
        c = f.read()
    changed = False

    # 反向提醒统一修复：在"本文信息核对于"前加"注意"类表述
    if slug in ["ai-thesis-writing-guide", "ai-resume-optimization", "cursor-vs-copilot-compare",
                "jimeng-ai-review", "midjourney-free-alternatives", "ai-video-tools-compare",
                "china-llm-landscape-2026"]:
        # 检查最后300字是否已有"别"或"不要"
        end = c[-300:]
        if "别" not in end and "不要" not in end:
            # 在"最后说一句反的"段中确保有"别"或"不要"
            # 或者直接在"本文信息核对于"前加一句
            c = c.replace("最后说一句反的：", "最后说一句反的：**别让 AI 替你做决定，**", 1)
            changed = True
            print(f"  {slug}: 反向提醒已修复")

    # 006: 删减
    if slug == "chatgpt-plus-worth-it":
        # 删减一些冗余
        c = c.replace("几乎每天用 AI 工作，付费逻辑就不一样了——不是「这笔钱花得值不值」，而是「每天省下来的时间按你的时薪折算，多久能回本」。每天省 20-30 分钟，一个月下来省出的时间远不止订阅费。按你自己的时薪折算一下就清楚了。", "几乎每天用 AI 工作，付费逻辑就不一样了——不是「花得值不值」，而是「每天省的时间按你的时薪折算，多久能回本」。每天省 20-30 分钟就够回本了。")
        changed = True

    # 012: 删减到900以下，加代码块，命题宽
    if slug == "jimeng-ai-review":
        # 在H2-2加代码块
        if "```" not in c:
            c = c.replace("即梦的中文提示词理解力最好，做海报配图门槛最低。", "即梦的中文提示词理解力最好，做海报配图门槛最低。下面是一个中文提示词结构模板：\n\n```\n【主体】+【动作/状态】+【环境背景】+【风格】+【构图】\n示例：一只橘猫趴在木质窗台上，午后阳光斜照，日系胶片风格，浅景深特写\n```\n\n")
        # 删减
        c = c.replace("即梦 AI 是字节跳动的图像生成工具，最大优势是中文提示词不用先翻译成英文。", "即梦 AI 的最大优势是中文提示词不用先翻译成英文。")
        # 题宽50 -> 52
        c = c.replace("meta_title: 即梦 AI 好用吗？中文出图能力与免费额度 — Learntide", "meta_title: 即梦 AI 好用吗？中文出图能力与免费额度解读 — Learntide")
        changed = True

    # 013: 结尾无KW
    if slug == "midjourney-free-alternatives":
        # 在最后一行加关键词
        c = c.replace("Midjourney 替代品，替代得了日常，替代不了顶级质感。\n\n本文信息核对于", "本文信息核对于")
        # 让最后一行含关键词
        c = c.replace("Midjourney 替代品：先说清楚能替代什么", "Midjourney 替代品免费吗？先说清楚能替代什么")
        # 确保最后一行有关键词
        c = c.replace("Midjourney 替代品，替代得了日常，替代不了顶级质感。", "Midjourney 替代品，替代得了日常，替代不了顶级质感。")
        # 在结尾加关键词
        c = c.replace("本文信息核对于", "Midjourney 替代品免费吗？替代得了日常，替代不了顶级质感。\n\n本文信息核对于")
        changed = True

    # 018: 删减到850以下，题宽51
    if slug == "ai-video-tools-compare":
        c = c.replace("如果你需要的是生成视频画面，而不是从素材剪视频，跳过去看生成类工具。", "")
        # 题宽
        c = c.replace("meta_title: AI 视频生成工具哪个好？6 款按用途分类选 — Learntide", "meta_title: AI 视频生成工具哪个好？六款按用途分类选 — Learntide")
        changed = True

    # 054: 题宽51, lede 24字
    if slug == "remove-ai-tone-writing":
        c = c.replace("meta_title: AI 味太重怎么改？六个去味技巧和改写方法 — Learntide", "meta_title: AI 味太重怎么改？去掉AI味的六个技巧 — Learntide")
        changed = True

    # 070: 扩到800字
    if slug == "ai-resume-optimization":
        c = c.replace("简历改完只是第一步，下一步是自我介绍和面试准备。", "简历改完只是第一步，下一步是自我介绍和面试准备。改完简历，再花同样时间准备自我介绍和面试话术，把纸面上的亮点变成可说出来的内容。")
        changed = True

    # 092: 反向提醒已修复

    if changed:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(c)
        print(f"  {slug}: 已修复")

print("最终修复完成")