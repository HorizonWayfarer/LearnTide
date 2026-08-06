# Learntide 第四批 10 篇 · 页面级 SEO 审计报告

审计人：欧化成（seo-optimizer）｜日期：2026-08-06
方法：读取 10 篇草稿 + `research/brief-*`；运行 `seo_probe_batch4.py`（密度/结构/链接/LSI/Schema）、`qa_check.py`（批次4 全 OK）、`meta_candidates_batch4.py`（meta 备选宽度机校验，全部 52–64 / 145–162 且含主词）。
批次4 在 `qa_check` 14 项硬标准上**全部通过**，但页面 SEO 仍有影响排名与收录质量的隐患。

---

## 一、总览评分表（五维各 20 分，合计 100）

| # | slug | 类型 | 主词 | 字数 | 密度 | **总分** | 关键词 | 结构 | 元信息 | 可读性 | 技术合规 | 结论 |
|---|------|------|------|-----:|-----:|:---:|:---:|:---:|:---:|:---:|:---:|------|
| 1 | gemini-free-plan-review | compare | gemini免费版怎么样 | 847 | 2.13% | **81** | 17 | 18 | 16 | 19 | 11 | 需补外链 |
| 2 | perplexity-ai-search-review | compare | perplexity怎么样 | 849 | 1.06% | **81** | 17 | 17 | 16 | 19 | 12 | 需补外链 |
| 3 | kling-vs-jimeng-compare | compare | 可灵和即梦哪个好 | 848 | 2.83% | **82** | 17 | 18 | 16 | 19 | 12 | 需补外链 |
| 4 | jianying-ai-features-review | compare | 剪映ai功能怎么样 | 777 | 2.70% | **74** | 14 | 16 | 13 | 19 | 12 | **返工** |
| 5 | ai-meeting-notes-tools | list | ai会议纪要工具 | 1093 | 1.65% | **81** | 17 | 18 | 16 | 19 | 11 | 需补外链/内链越位 |
| 6 | ai-meeting-minutes-guide | tutorial | ai整理会议纪要 | 893 | 2.02% | **74** | 17 | 17 | 16 | 18 | 6 | **返工** |
| 7 | avoid-ai-hallucination-tips | tutorial | ai胡说八道怎么办 | 886 | 2.37% | **74** | 15 | 17 | 16 | 19 | 7 | **返工** |
| 8 | jianying-ai-tutorial | tutorial | 剪映ai怎么用 | 892 | 1.68% | **74** | 17 | 17 | 16 | 18 | 6 | **返工** |
| 9 | suno-ai-tutorial-cn | tutorial | suno怎么用 | 857 | 1.05% | **75** | 17 | 17 | 16 | 18 | 7 | **返工** |
| 10 | ai-mock-interview-guide | tutorial | ai模拟面试 | 839 | 1.43% | **75** | 16 | 18 | 16 | 18 | 7 | **返工** |

**共性拖累项**：① 全 10 篇 0 条外链（违反 B5：需 ≥2 条权威一手源）；② 全 10 篇 meta_description 不含精确主词；③ 5 篇教程正文内链 0 条（违反 B4：H2 第 2–4 需 ≥1 内链）；④ 5 篇正文散文误用半角 `"`（应统一「」）；⑤ Schema 仅 Article+BreadcrumbList，未用 FAQ/HowTo。

---

## 二、需返工文章（6 篇）

- **jianying-ai-features-review** — H1/meta_title 主词错配（现用「好用吗」替代「功能怎么样」）+ 缺对比表 + 0 外链。
- **ai-meeting-minutes-guide** — 0 内链 + 11 处半角引号 + 「五步」措辞与正文 4 个步骤 H2 不一致 + 0 外链。
- **avoid-ai-hallucination-tips** — 0 内链 + 4 处半角引号 + LSI 偏弱（缺「幻觉/编造/提示词」）+ 0 外链。
- **jianying-ai-tutorial** — 0 内链 + 11 处半角引号 + 0 外链。
- **suno-ai-tutorial-cn** — 0 内链 + 4 处半角引号 + 密度偏低(1.05%) + 0 外链。
- **ai-mock-interview-guide** — 0 内链 + 6 处半角引号 + LSI 缺「提示词」+ 0 外链。

轻量修订（换 meta + 补链接即可，不必返工草稿）：gemini / perplexity / kling / meeting-notes — 仅需补外链 + 替换含主词 meta_description + 内链配额微调。

---

## 三、发布前必修清单（按优先级）

**P0 · 阻断级**
1. **外链 B5：全 10 篇 0 条外链** → 每篇补 ≥2 条权威一手源（官网/官方文档/帮助中心）。本批最大硬伤，单独一条即拖累 E-E-A-T。
2. **正文内链 B4：5 篇教程（#6/#7/#8/#9/#10）正文内链 0 条** → 在 H2 第 2–3 节各加 ≥1 条内链（#6→#5、#8→#4 等）。
3. **jianying-ai-features H1/meta_title 主词错配** → 必须含精确主词「功能怎么样」（现用「好用吗」），否则主词排名承接失效。

**P1 · 高优**
4. **半角引号规范**：#6(11)、#8(11)、#10(6)、#9(4)、#7(4) 正文散文误用 `"`，统一改为「」（代码块内提示词可保留半角）。
5. **meta_description 全 10 篇缺主词** → 全部替换为含主词备选（宽度已校验 145–162，见第五节）。
6. **ai-meeting-minutes 步数措辞** → 标题/描述写「五步」，正文仅 4 个步骤 H2（第四步含五条清单），统一为「四步」。
7. **Schema 补 FAQ/HowTo**：#6/#8/#9/#10 加 HowTo；#7 加 FAQPage；#1/#2/#4 可加 FAQPage。

**P2 · 中优**
8. **LSI/长尾覆盖**：#7 仅 4/7（补「幻觉/编造/提示词」）、#10 仅 6/7（补「提示词」1 次）。
9. **密度微调**：#9 1.05% 偏低，正文自然加 1–2 次主词；#3/#4 2.7–2.83% 略高但长尾主词可接受，无需降。
10. **内链越位/超配额**：#1 内链 3 落在 [4,5,5]、#5 内链 3 落在 [2,5,5] → 收到 1–2 条并移入 H2 第 2–3；#3 位置 [3,5] 留 1 条在第 3 即可。

---

## 四、Meta 标题/描述推荐（每篇 A 选，均含精确主词、宽度已校验）

| slug | meta_title（A 选） | meta_description（A 选，含主词） |
|---|---|---|
| gemini-free-plan-review | Gemini 免费版怎么样？额度、三个短板和适用人群 | Gemini 免费版怎么样？日常问答和读图撑得住，真正卡人的是无声降档。讲清免费用到什么、三个绕不开的短板与国内两道坎，哪些人根本不用升级，附省额度提问模板。 |
| perplexity-ai-search-review | Perplexity 怎么样？AI 搜索的优点、短板和适用人群 | Perplexity 怎么样？带引用的 AI 搜索，答案能点回原文核对。说清三个好用的地方、中文语料偏弱等三个短板，再按查海外资料、竞品调研、写论文给推荐度，讲明谁值得付费。 |
| kling-vs-jimeng-compare | 可灵和即梦哪个好？AI 视频生成七个维度对比 | 可灵和即梦哪个好？概念片走可灵，口播和电商动效走即梦。本文用七个维度对比文生视频、图生视频、口型对嘴和免费额度，按三类用途给选择建议，并列出四个新手最常踩的坑。 |
| jianying-ai-features-review | 剪映 AI 功能怎么样？值得用的和建议别碰的 | 剪映 AI 功能怎么样？把那一排按钮分成值得用、看情况、建议别碰三档，逐项说明适用场景与翻车条件，讲清免费与会员的大致边界，并给出发布前清单和三条建议。 |
| ai-meeting-notes-tools | AI 会议纪要工具怎么选？4 款中文场景实测对比 | AI 会议纪要工具分转写层和纪要生成层，选错多半是把两层混为一谈。本文对比飞书妙记、腾讯会议 AI、通义听悟和组合流的中文识别、说话人区分与免费边界，按会议场景给建议。 |
| ai-meeting-minutes-guide | 用 AI 整理会议纪要：从录音到待办的四步流程 | 用 AI 整理会议纪要，四步把录音变成能发出去的成品：先转写再清洗逐字稿，用完整提示词生成结论与待办表，按五条清单核对，另附录音太长、抢话、口音重处理法。 |
| avoid-ai-hallucination-tips | AI 胡说八道怎么办？五个立刻能用的防错习惯 | AI 胡说八道怎么办？模型不是在检索资料，是在按概率猜字，所以编出来的东西特别像真的。五个防错习惯配可复制句式，另列出数字、法条、引用等五类看到就必须核对的内容。 |
| jianying-ai-tutorial | 剪映 AI 怎么用？从智能成片到自动字幕全流程 | 剪映 AI 怎么用？手机端和电脑端的入口分别在哪、按钮找不到时先排查什么、智能成片四步操作、自动字幕必改三类词、口播正确顺序，及三个翻车处理和免费边界。 |
| suno-ai-tutorial-cn | Suno 怎么用？从中文歌词到成品歌的完整教程 | Suno 怎么用？从注册到出第一首歌的完整步骤，附中文咬字优化的五个实用技巧、风格提示词公式与三个可复制示例、歌词结构标签模板，以及免费额度和商用边界。 |
| ai-mock-interview-guide | AI 模拟面试怎么练？三轮练习法和可复制提示词 | AI 模拟面试三轮练出手感：岗位拆解出高概率问题、压力追问逼出真实反应、复盘打分给改进方向，附三段可复制提示词、一张评分维度表，以及简历脱敏和真实性方面的注意。 |

---

## 五、B5 外链目标建议（权威一手源，落地前人工核验域名）

| slug | 建议外链目标（均为官方根域） |
|------|------|
| gemini-free-plan-review | gemini.google.com、support.google.com/gemini |
| perplexity-ai-search-review | perplexity.ai、docs.perplexity.ai |
| kling-vs-jimeng-compare | klingai.com、dreamina.capcut.com（即梦官网） |
| jianying-ai-features-review | lv.ulikecam.com（剪映官网）、剪映帮助中心 |
| ai-meeting-notes-tools | 飞书妙记、腾讯会议 AI 小助手、通义听悟 官方页 |
| ai-meeting-minutes-guide | otter.ai / 飞书妙记 官网 |
| avoid-ai-hallucination-tips | OpenAI / Google 模型说明或安全文档 |
| jianying-ai-tutorial | lv.ulikecam.com（剪映官网） |
| suno-ai-tutorial-cn | suno.com、docs.suno.com |
| ai-mock-interview-guide | 主流面试/求职平台说明文档 |

⚠️ 避开仿冒镜像站：suno-zh.com、suno.cn、gemini-pro.cn 等。中文工具域名务必核验解析到官方站再落链。

---

**交付物状态**：meta 备选已机器校验（题宽 52–64、述宽 145–162、均含精确主词）；探针数据见 `seo4.json`；meta 生成器见 `reports/meta_candidates_batch4.py`。
