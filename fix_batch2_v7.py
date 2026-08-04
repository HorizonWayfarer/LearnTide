# -*- coding: utf-8 -*-
"""精准修复v7: 只修剩余FAIL项"""
import re

# 006: lede 27字, lede重复
c = open("drafts/chatgpt-plus-worth-it.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 订阅前先按频率分档，不同用法对应不同答案，对号入座就能算出值不值。", c, flags=re.M)
open("drafts/chatgpt-plus-worth-it.md", "w", encoding="utf-8", newline="\n").write(c)

# 012: 字数915, 无代码块(代码块在\`\`\`之间但qa_check没识别到)
c = open("drafts/jimeng-ai-review.md", encoding="utf-8").read()
# 删减
c = c.replace("它的风格化输出适合日常，但高要求输出仍是 Midjourney 领先。", "风格化输出适合日常，高要求输出仍是 Midjourney 领先。")
# 加一个真正的代码块
c = c.replace("它是积分制、每天刷新免费额度。", "它是积分制、每天刷新免费额度。\n\n```\n使用模板：主体+动作+环境+风格+构图\n示例：橘猫趴在窗台，午后阳光，日系胶片，浅景深\n```\n\n")
open("drafts/jimeng-ai-review.md", "w", encoding="utf-8", newline="\n").write(c)

# 013: 字数882, 结尾无KW, lede 28字, lede重复
c = open("drafts/midjourney-free-alternatives.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 想找免费替代品先搞清楚替代得了什么，日常出图可以，顶级质感不行。", c, flags=re.M)
# 确保结尾有关键词 - 最后一行
c = c.replace("本文信息核对于", "Midjourney 替代品适合日常出图，不适合顶级质感。\n\n本文信息核对于")
open("drafts/midjourney-free-alternatives.md", "w", encoding="utf-8", newline="\n").write(c)

# 018: 字数856, 题宽51, lede重复
c = open("drafts/ai-video-tools-compare.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 搜 AI 视频工具会搜到一堆名字，但文生视频、图生视频、AI 剪辑是三件不同的事。", c, flags=re.M)
c = c.replace("它们属于三个不同类别，不搞清楚就选肯定错。", "它们属于三个不同类别，不搞清楚就选会踩坑。")
open("drafts/ai-video-tools-compare.md", "w", encoding="utf-8", newline="\n").write(c)

# 029: lede 28字
c = open("drafts/cursor-vs-copilot-compare.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 选 Cursor 还是 Copilot 不是比谁更强，而是看你的场景是改单个文件还是改整个项目。", c, flags=re.M)
open("drafts/cursor-vs-copilot-compare.md", "w", encoding="utf-8", newline="\n").write(c)

# 053: lede重复
c = open("drafts/ai-prompt-formula-template.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 记不住复杂提示词技巧，记住五个填空就能写出好指令，这就是公式的价值。", c, flags=re.M)
open("drafts/ai-prompt-formula-template.md", "w", encoding="utf-8", newline="\n").write(c)

# 054: 题宽49, lede重复
c = open("drafts/remove-ai-tone-writing.md", encoding="utf-8").read()
c = c.replace("meta_title: AI 味太重怎么改？六个去AI味技巧和方法 — Learntide", "meta_title: AI 味太重怎么改？六个去掉AI味的技巧和方法 — Learntide")
c = re.sub(r"^lede: .+$", "lede: AI 写的东西一眼就能看出是机器写的，因为排比泛滥、缺少细节、每段总结，这是三个具体特征。", c, flags=re.M)
c = c.replace("认出这四个特征，就知道从哪下手改。", "认出这些特征，就知道从哪下手改。")
open("drafts/remove-ai-tone-writing.md", "w", encoding="utf-8", newline="\n").write(c)

# 070: lede重复
c = open("drafts/ai-resume-optimization.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 简历投了很多没回音，不是因为经历不够，而是只记录了职责没写出成果，这是最关键的问题。", c, flags=re.M)
c = c.replace("关键问题在于只记录了职责，没写出成果。", "问题在于只记录了职责，没写出成果。")
open("drafts/ai-resume-optimization.md", "w", encoding="utf-8", newline="\n").write(c)

print("done")