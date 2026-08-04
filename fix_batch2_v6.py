# -*- coding: utf-8 -*-
"""精准修复每个FAIL"""
import re, os

# 006: lede 22字 -> 33字, lede重复 -> 用正文不出现的话
c = open("drafts/chatgpt-plus-worth-it.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 决定要不要订阅 ChatGPT Plus 之前，先搞清楚自己属于哪一档使用频率，再算账。", c, flags=re.M)
c = c.replace("ChatGPT Plus 值得开吗，没有统一答案，先看自己一周用几次再算账。", "(本文从频率分档角度帮你判断)")  # 确保正文不出现lede原文
c = c.replace("(本文从频率分档角度帮你判断)", "本文从频率分档角度帮你判断")
open("drafts/chatgpt-plus-worth-it.md", "w", encoding="utf-8", newline="\n").write(c)

# 012: 字数921/900, 无代码块
c = open("drafts/jimeng-ai-review.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 即梦 AI 是字节跳动出品的免费中文出图工具，国内直接可用，中文提示词不用翻译成英文。", c, flags=re.M)
# 重复了"国内直接可用"，改正文
c = c.replace("国内直接可用，没有海外工具的网络门槛。", "没有海外工具的网络门槛。")
# 删除一些冗余
c = c.replace("即梦的中文提示词理解力最好。下面是一个中文提示词模板：", "下面是一个中文提示词模板：")
open("drafts/jimeng-ai-review.md", "w", encoding="utf-8", newline="\n").write(c)

# 013: 字数887/850, 结尾无KW, 无反向提醒, lede 21字
c = open("drafts/midjourney-free-alternatives.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 想找 Midjourney 的免费替代品，先搞清楚替代得了什么、替代不了什么，再挑工具。", c, flags=re.M)
# 去掉重复的"替代得了日常替代不了顶级质感"
c = c.replace("免费替代品，替代得了日常，替代不了顶级质感。", "")
# 反向提醒加"别"
c = c.replace("最后说一句反的：", "最后说一句反的：**别打着免费替代的名义凑合，**", 1)
# 删除多余的结尾关键词行
c = c.replace("记住，Midjourney 替代品适合日常，替代不了顶级质感。\n\n本文信息核对于", "本文信息核对于")
# 删减
c = c.replace("先把下面这条提示词发给 AI，它能帮你把 Midjourney 提示词转成中文工具能用的格式：", "把下面这条提示词发给 AI，它能帮你转格式：")
open("drafts/midjourney-free-alternatives.md", "w", encoding="utf-8", newline="\n").write(c)

# 018: 字数856/850, 题宽51, lede 28字
c = open("drafts/ai-video-tools-compare.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 搜 AI 视频工具会搜到一堆名字，但文生视频、图生视频、AI 剪辑是三件完全不同的事。", c, flags=re.M)
c = c.replace("搜 AI 视频工具会搜到一堆名字，但它们在做三件完全不同的事，先分清。", "它们属于三个不同类别，不搞清楚就选肯定错。")
open("drafts/ai-video-tools-compare.md", "w", encoding="utf-8", newline="\n").write(c)

# 029: lede 28字, 无反向提醒
c = open("drafts/cursor-vs-copilot-compare.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 选 Cursor 还是 Copilot，不是比谁更强，是看你的场景是改单个文件还是改整个项目。", c, flags=re.M)
c = c.replace("这两个不是同一类东西。选哪个取决于你想改的是一个文件还是一整个项目。", "它们一个插在现有编辑器里用，一个要你换编辑器。")
# 反向提醒
c = c.replace("最后说一句反的：", "最后说一句反的：**别让工具选你，**", 1)
open("drafts/cursor-vs-copilot-compare.md", "w", encoding="utf-8", newline="\n").write(c)

# 053: lede重复
c = open("drafts/ai-prompt-formula-template.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 提示词模板公式就是五个空：角色、任务、背景、格式、约束，填完就是一条可以直接用的指令。", c, flags=re.M)
c = c.replace("提示词模板公式就五个空：角色、任务、背景、格式、约束，填完就是一条好指令。", "记不住复杂技巧，记住五个空就够了。")
open("drafts/ai-prompt-formula-template.md", "w", encoding="utf-8", newline="\n").write(c)

# 054: 题宽49, lede 25字
c = open("drafts/remove-ai-tone-writing.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: AI 写的东西一眼就能看出是机器写的，因为排比多、没细节、爱总结，这是四个很具体的特征。", c, flags=re.M)
c = c.replace("AI 味不是玄学，它有四个特征，认出来改起来就快，用对方法就行。", "认出这四个特征，就知道从哪下手改。")
open("drafts/remove-ai-tone-writing.md", "w", encoding="utf-8", newline="\n").write(c)

# 070: lede 29字
c = open("drafts/ai-resume-optimization.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 简历投了很多没回音，不是经历不够，是只写了做过什么，没写做成了什么，这是最关键的问题。", c, flags=re.M)
c = c.replace("简历投了很多没回音，不是经历不够，是只写了做什么没写做成了什么。", "关键问题在于只记录了职责，没写出成果。")
open("drafts/ai-resume-optimization.md", "w", encoding="utf-8", newline="\n").write(c)

# 092: lede 27字
c = open("drafts/china-llm-landscape-2026.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 国产大模型名字听过一堆但分不清谁是谁家的、各自擅长什么，一张表加三个分类就能看懂格局。", c, flags=re.M)
c = c.replace("国产大模型有哪些、谁家出的、怎么挑，一张表就能看懂，不用记跑分。", "不用记跑分，按厂商归属和用途分类就能看懂。")
open("drafts/china-llm-landscape-2026.md", "w", encoding="utf-8", newline="\n").write(c)

print("精准修复完成")