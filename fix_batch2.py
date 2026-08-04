# -*- coding: utf-8 -*-
"""批量修复第2批文章：H2关键词、结尾关键词、lede"""
import re, os

fixes = {
    "chatgpt-plus-worth-it": {
        "h2": {"先分档：你属于哪一类使用频率": "ChatGPT Plus 值得开吗？先分档看使用频率"},
        "end": "不确定自己值不值得开，把下面这段发给任意一个 AI 让它替你判断。ChatGPT Plus 值得开吗，关键是按频率分档算自己那一档。",
        "lede": "这个问题没有统一答案，取决于你一周用几次。ChatGPT Plus 值得开吗，先对号入座再算账。",
    },
    "jimeng-ai-review": {
        "h2": {"先定位：中文提示词友好的免费出图工具": "即梦 AI 好用吗？先搞清楚它能做什么"},
        "end": "即梦 AI 好用吗，适合日常出图，不适合精细商用。免费工具在这些方面有取舍是正常的。",
        "lede": "如果你要的是打开就能用、中文说人话就能出图，即梦是目前门槛最低的。",
    },
    "midjourney-free-alternatives": {
        "h2": {"先说清楚：替代得了什么，替代不了什么": "Midjourney 替代品：先说清楚能替代什么"},
        "end": "需要顶级质感，Midjourney 的订阅费不该省。Midjourney 替代品，适合日常替代，替代不了顶级质感。",
        "lede": "替代得了日常，替代不了顶级质感。先把这个诚实定调放前面，再看具体工具。",
    },
    "ai-video-tools-compare": {
        "h2": {"先分清三类：文生视频 / 图生视频 / AI 剪辑": "AI 视频生成工具哪个好？先分清三类再选"},
        "end": "别接超出工具能力的活。AI 视频生成工具哪个好，取决于你要做的是哪种视频。",
        "lede": "搜 AI 视频工具会搜到一堆名字，但它们其实在做三件不同的事。先分清三类，再选工具。",
    },
    "cursor-vs-copilot-compare": {
        "h2": {"结论先行：改单文件选 Copilot，改整个项目选 Cursor": "Cursor 和 Copilot 哪个好？一句话分流"},
        "end": "Cursor 和 Copilot 哪个好，取决于你的瓶颈是打字慢还是读代码慢。选错工具，两个都会觉得不值。",
        "lede": "这两个不是同一类东西。选哪个取决于你想改的是一个文件还是一整个项目。",
    },
    "ai-thesis-writing-guide": {
        "h2": {"先划红线：哪些算学术不端，哪些是正常工具使用": "AI 写论文怎么用才不算作弊？先划红线"},
        "end": "AI 写论文怎么用，关键在守住思考的边界。想知道为什么 AI 会编造，可以看看大模型是什么那篇里讲的原因。",
        "lede": "用不用 AI 不是问题，用在哪个环节才是。AI 写论文，帮你找文献没问题，替你写论点就越界了。",
    },
    "ai-prompt-formula-template": {
        "h2": {"一个公式打底": "提示词模板公式：一个公式打底"},
        "end": "提示词模板公式，核心就是五段填空。公式解决的是说清楚，不解决你自己也没想清楚要什么。",
        "lede": "记不住一堆提示词技巧？用一个公式就够了。提示词模板公式，核心就是五段填空。",
    },
    "remove-ai-tone-writing": {
        "h2": {"先认出 AI 味：四个典型特征": "AI 味太重怎么改？先认出四个特征"},
        "end": "AI 味太重怎么改，认出特征，用对方法，就能改好。去味不等于去错误，内容本身还是要核实。",
        "lede": "AI 味不是玄学，它有四个很具体的特征。认出来了，改起来就快。",
    },
    "ai-resume-optimization": {
        "h2": {"简历没回音的真正原因": "AI 优化简历：先找到没回音的真正原因"},
        "end": "用 AI 优化简历，核心是让 AI 帮你把经历说清楚，不是替你编经历。改完简历，用同样的素材准备面试，效果才能落地。",
        "lede": "投了很多没回音，多半不是经历不够，是简历只写了做过什么，没写做成了什么。",
    },
    "china-llm-landscape-2026": {
        "h2": {"一张表看清主要玩家": "国产大模型有哪些？一张表看清主要玩家"},
        "end": "国产大模型有哪些，记住按厂商和用途分类就够了。先明确你要做什么，再挑对应的工具。",
        "lede": "名字听过一堆但分不清谁是谁家的、各自擅长什么？一张表看清楚国产大模型有哪些。",
    },
}

for slug, f in fixes.items():
    path = f"drafts/{slug}.md"
    if not os.path.isfile(path):
        print(f"!! {slug}: 文件不存在")
        continue
    with open(path, encoding="utf-8") as fh:
        c = fh.read()
    changed = False
    for old_h2, new_h2 in f.get("h2", {}).items():
        if old_h2 in c:
            c = c.replace(old_h2, new_h2, 1)
            changed = True
            print(f"  {slug}: H2 已修复")
        else:
            print(f"  !! {slug}: H2 未找到: {old_h2[:30]}")
    if "end" in f:
        c = c.replace("最后说一句反的：", f["end"] + "\n\n最后说一句反的：", 1)
        changed = True
        print(f"  {slug}: 结尾已修复")
    if "lede" in f:
        c = re.sub(r"^lede: .+$", "lede: " + f["lede"], c, flags=re.M)
        changed = True
        print(f"  {slug}: lede 已修复")
    if changed:
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(c)
        print(f"  {slug}: 已保存")

print("批量修复完成")