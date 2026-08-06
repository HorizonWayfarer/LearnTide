---
id: 057
slug: midjourney-prompt-tips
title: Midjourney 提示词怎么写？结构拆解
category: 使用教程
article_type: tutorial
primary_keyword: midjourney提示词怎么写
meta_title: Midjourney 提示词怎么写？结构拆解与参数说明 — Learntide
meta_description: Midjourney 提示词怎么写？本文拆解主体、场景、风格、构图、光影、参数六段结构，说明 --ar、--stylize 等参数怎么用，并给出可直接复制的模板与两个示例。
lede: 出图不靠运气靠结构：主体场景写清楚，风格构图光影跟上，参数最后调，模板直接套。
internal_links:
  - slug: midjourney-free-alternatives
    anchor: Midjourney 的免费替代品
  - slug: jimeng-ai-review
    anchor: 即梦 AI 好用吗
  - path: ../tools.html
    anchor: AI 工具导航
  - slug: fix-ai-hands-generation
    anchor: AI 画手修复教程
date: 2026-08-04
verified: 2026-08-05
---

## Midjourney 提示词怎么写？先给六段结构

Midjourney 提示词怎么写？先记一句话：主体、场景、风格、构图、光影、参数。这六段各管一件事，把顺序记熟，出图质量立刻上一个台阶。大多数人出的图「不是想要的感觉」，问题就出在结构乱——要么主体没写清，要么参数乱堆。下面逐段拆解，最后给一个可直接套用的模板，复制改词就能用。先把这段结构背下来，比收集一百条咒语有用得多。出图是门手艺，但多数翻车都是结构问题，不是运气问题。

## 逐段拆解：每段该写什么

主体放最前，也最重要，写「谁、在做什么」，比如「a woman in a raincoat」。场景是环境，「on a neon-lit street」。风格决定画风，「cinematic / oil painting / 3D render」任选。构图管视角，「close-up / wide shot / centered」。光影和情绪放一起，「golden hour / moody」。每段给一两个词就够，别贪多。堆一堆形容词，不如把主体写具体。记住：一句话能说清画面，就不要堆成一段。写提示词不是写作文，信息密度高才有效。

## 参数怎么用：--ar / --stylize / --chaos / --no

参数是锦上添花，不是越多越好。核心四个：

| 参数 | 作用 | 建议取值 |
|---|---|---|
| --ar | 画面比例 | 16:9、2:3、1:1 |
| --stylize | 风格化强度 | 0–1000，常用 250–750 |
| --chaos | 随机变化 | 0–100，低更稳 |
| --no | 排除元素 | 写不想出现的东西 |

版本号会更新，写法以当前版本为准。先保证主体和场景写清楚，参数是加分项，不是救命稻草。参数加太多，反而容易让画面失控。这四个参数是最高频的，先会用它们，再研究更冷门的。比例决定构图空间，风格化决定画面艺术感，随机度决定每次差异，排除词决定画面里不出现什么，各管一摊。

## 一个可直接套用的模板 + 两个示例

下面模板直接复制，把【】里的内容换成自己的需求。示例一是产品图，示例二是电影感人像，照结构改就能用。

```
【主体及动作】，【场景/环境】，【风格：如 cinematic / oil painting / 3D render】，
【构图：close-up / wide shot / centered】，【光影：golden hour / rim light】，【情绪/色彩】
--ar 【比例，如 16:9】 --stylize 【0-1000，常用 250-750】 --no 【不要出现的内容】
```

```
【示例·产品图】a minimalist wireless earbuds product shot, studio lighting,
clean white background, centered, soft shadows --ar 1:1 --stylize 400

【示例·电影感人像】a woman in a raincoat on a neon-lit street, cinematic,
85mm lens, shallow depth of field, teal and orange grade, moody --ar 2:3 --stylize 250
```

两个示例的区别在风格和参数：产品图求干净，风格化给到 400 已经够；人像要氛围，光影词和胶片感参数一起上。照着这个思路，换成你自己的主体就能用。先把主体换掉，再调风格词，最后微调参数，一次只动一处，方便看出是哪里起的作用。

## 三个常见错误

过度堆砌形容词，十来个形容词不如一个清晰的主体。忽略参数，比例和风格化不设，出图全凭运气。主体太多，一个画面塞三四个主角，AI 只能乱来。注意：这套结构适用于 Midjourney，[Stable Diffusion](https://stability.ai){:target="_blank"}、[即梦](https://jimeng.jianying.com){:target="_blank"}等中文工具语法不同，别照搬。它需要付费订阅，国内访问可能要额外网络条件，介意的话可以看[Midjourney 的免费替代品](midjourney-free-alternatives.html)那篇。把这三个错误记熟，能避开大多数翻车现场。

工具价格与免费额度可能变动，实际以各工具官网当前说明为准。
Midjourney 提示词怎么写？六段结构记熟，但参数不是越多越好，别把中文工具的语法硬套进来。
