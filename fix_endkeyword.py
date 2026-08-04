# -*- coding: utf-8 -*-
"""修复结尾关键词：在「本文信息核对于」行后追加含关键词的收尾句"""
import re, os

articles = {
    "chatgpt-plus-worth-it": "ChatGPT Plus 值得开吗，按频率分档算自己那档就有答案。",
    "jimeng-ai-review": "即梦 AI 好用吗，适合日常出图，不适合精细商用。",
    "midjourney-free-alternatives": "Midjourney 替代品，替代得了日常，替代不了顶级质感。",
    "ai-video-tools-compare": "AI 视频生成工具哪个好，先分清三类，再选工具。",
    "cursor-vs-copilot-compare": "Cursor 和 Copilot 哪个好，取决于你的瓶颈是打字慢还是读代码慢。",
    "ai-thesis-writing-guide": "AI 写论文怎么用，关键在守住思考的边界。",
    "ai-prompt-formula-template": "提示词模板公式，核心就是五段填空。",
    "remove-ai-tone-writing": "AI 味太重怎么改，认出特征，用对方法，就能改好。",
    "ai-resume-optimization": "用 AI 优化简历，核心是让 AI 帮你把经历说清楚，不是替你编经历。",
    "china-llm-landscape-2026": "国产大模型有哪些，记住按厂商和用途分类就够了。",
}

for slug, end_line in articles.items():
    path = f"drafts/{slug}.md"
    with open(path, encoding="utf-8") as f:
        c = f.read()
    
    # 替换结尾
    marker = "本文信息核对于 2026-08，工具价格与额度可能变动。"
    old_end = marker
    new_end = marker + "\n" + end_line
    
    if old_end in c:
        c = c.replace(old_end, new_end, 1)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(c)
        print(f"  {slug}: 结尾关键词已修复")
    else:
        print(f"  !! {slug}: 未找到结尾标记")

print("完成")