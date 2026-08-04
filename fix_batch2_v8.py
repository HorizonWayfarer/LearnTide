# -*- coding: utf-8 -*-
"""修复剩余4篇FAIL"""
import re

# 012: 字数915/900, 无代码块
c = open("drafts/jimeng-ai-review.md", encoding="utf-8").read()
c = c.replace("即梦 AI 是字节跳动的图像生成工具，最大优势是中文提示词不用先翻译成英文。", "即梦 AI 最大优势是中文提示词不用先翻译成英文。")
c = c.replace("它采用积分制，每天刷新免费额度，对日常使用来说够用。", "它采用积分制，每天刷新免费额度，日常够用。")
# 加代码块
c = c.replace("擅长：风格化插画、中文场景理解（古诗意境、节日海报、国风元素）、日常配图生成。", "擅长：风格化插画、中文场景理解、日常配图生成。\n\n```\n提示词：橘猫趴在窗台，午后阳光，日系胶片，浅景深\n```\n\n")
open("drafts/jimeng-ai-review.md", "w", encoding="utf-8", newline="\n").write(c)

# 013: 字数898/850, 结尾无KW, lede 29字, 无反向提醒
c = open("drafts/midjourney-free-alternatives.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 找 Midjourney 免费替代品前先想清楚替代得了什么，日常出图可以，顶级质感不行。", c, flags=re.M)
# 删减
c = c.replace("选哪款取决于你的核心需求。日常配图社交媒体系列，即梦或可灵足够。精细控制需求、愿意投入时间学习，Stable Diffusion 本地部署最省钱。已经在用 ChatGPT 的，DALL·E 3 随对话出图最方便。需要顶级质感，Midjourney 仍是首选。", "日常配图即梦或可灵足够，精细控制需求选 Stable Diffusion 本地部署，已经在用 ChatGPT 的选 DALL·E 3，需要顶级质感仍是 Midjourney。")
# 结尾关键词
c = c.replace("Midjourney 替代品适合日常出图，不适合顶级质感。\n\n本文信息核对于", "本文信息核对于")
c = c.replace("Midjourney 替代品，替代得了日常，替代不了顶级质感。", "Midjourney 替代品，替代得了日常，替代不了顶级质感。")
# 反向提醒
c = c.replace("最后说一句反的：", "最后说一句反的：**别让免费替代品浪费你的时间，**", 1)
open("drafts/midjourney-free-alternatives.md", "w", encoding="utf-8", newline="\n").write(c)

# 018: 字数856/850, 题宽51, lede重复
c = open("drafts/ai-video-tools-compare.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 搜 AI 视频工具会搜到一堆名字，但文生视频、图生视频、AI 剪辑是三类完全不同的事。", c, flags=re.M)
c = c.replace("它们属于三个不同类别，不搞清楚就选会踩坑。", "它们属于三个不同类别，不搞清楚就选会踩坑。")
# 删减6字
c = c.replace("用途完全不同，按排名榜单从上往下挑必然选错。", "")
# 题宽修复
c = c.replace("meta_title: AI 视频生成工具哪个好？六款按用途分类选 — Learntide", "meta_title: AI 视频生成工具怎么选？六款按用途分类推荐 — Learntide")
open("drafts/ai-video-tools-compare.md", "w", encoding="utf-8", newline="\n").write(c)

# 029: lede 29字
c = open("drafts/cursor-vs-copilot-compare.md", encoding="utf-8").read()
c = re.sub(r"^lede: .+$", "lede: 选 Cursor 还是 Copilot 不是比谁更强，而是看你的场景是改单个文件还是改整个项目结构。", c, flags=re.M)
open("drafts/cursor-vs-copilot-compare.md", "w", encoding="utf-8", newline="\n").write(c)

print("done")