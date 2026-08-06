# LearnTide 收尾批（第 11 批）SEO 技术审计报告

> 审计日期：2026-08-06
> 审计人：seo-optimizer-4（欧化成）
> 审计范围：收尾批 10 篇（已通过 qa_check 0 FAIL，已构建上线，全站共 113 篇内容，100 篇规划全部覆盖）
> 报告路径：`A:\LearnTide\reports\seo-report-batch11-2026-08-06.md`
> 对标标准：延续第 8/9/10 批口径——密度以规范化命中（忽略大小写/空格）为分子、正文中文字数为分母；Meta 宽度为显示宽度（CJK×2），题宽 52–64 / 述宽 145–162；外链仅认官方/权威域名，仿冒镜像不得链入。

---

## 一、批级 SEO 评分

### 综合评分：89 / 100 — ✅ 合格（无 P0，综合 ≥70）

> 判定：收尾批 10 篇 **0 个 P0**。禁词「实测/待核实/TODO/通义灵码/上下文窗口/SWE-bench」全批 0 命中；仿冒镜像零链入；外链全为官方/权威域名且 DNS/实测有效；法律话题软表述、无编造数字。按「无 P0 且综合 ≥70 才算合格」标准，**本批判定为合格（Ready to Publish）**。存在 1 项 P1 建议修复（6 篇 Meta 未含精确主词），不影响发布资格。

| 维度 | 得分 | 满分 | 说明 |
|------|------|------|------|
| 关键词优化 | 17 | 25 | 前 100 字覆盖 10/10 ✅；H2 含主词 10/10 满足最低 1（理想 2 仅 0 篇）；密度规范化 4/10 达 ≥1.00%（chart 1.12、career 1.07、hallucination 1.00、beginner 1.00），4 篇 0.90–0.99% 临界，2 篇 <0.90%（distillation 0.89、labeling 0.89） |
| 内容质量与精选摘要 | 22 | 25 | 全批结论前置 + 直答段 + 关键要点/表格/提示词块，精选摘要机会 10/10 优良 |
| Meta 元素 | 21 | 25 | 题宽 10/10（53–63）、述宽 10/10（145–157）全部合格；⚠️ 6 篇 Meta Description、4 篇 Meta Title 未含精确主词（P1-1，详见 Meta 优化建议） |
| 结构与链接 | 20 | 25 | 内链 10/10 无断链（含 ai-weekly-report-guide.html 已上线）；外链 10/10 全官方且 DNS/实测有效（含 arxiv.org Hinton 论文 ✅）；外链数 2 条/篇达标 |
| 诚信合规 | 25 | 25 | **P0=0**；禁词全批 0；仿冒镜像未链入；deepfake 软表述「据公开报道」无编造数字；labeling 新规日期与官方全文一致；hallucination 禁词铁律 0 命中（无「上下文窗口」「SWE-bench」，用「记性空间」） |

---

## 二、逐篇评分表

| # | 文章 | ID | 密度(规范化) | 前100 | H2含主词 | 题宽 | 述宽 | 外链(官方) | 主词入Meta | P0 | 综合 |
|---|------|-----|-------------|-------|---------|------|------|-----------|-----------|-----|------|
| 1 | ai-expense-tracking-guide | 076 | 0.92% ⚠️ | ✓ | 1/5 | 62 ✅ | 147 ✅ | 2（pay.weixin.qq.com、feidee.com）✅ | MT✅ MD✅ | 无 | 90 |
| 2 | ai-chart-generation-guide | 079 | 1.12% ✅ | ✓ | 1/5 | 62 ✅ | 154 ✅ | 2（support.microsoft.com、ai.wps.cn）✅ | MT✅ MD✅ | 无 | 92 |
| 3 | local-ai-model-setup | 080 | 0.99% ⚠️ | ✓ | 1/5 | 63 ✅ | 150 ✅ | 2（ollama.com、github.com/ollama）✅ | MT✅ MD✅ | 无 | 91 |
| 4 | what-is-ai-hallucination | 083 | 1.00% ✅ | ✓ | 1/5 | 63 ✅ | 157 ✅ | 2（platform.openai.com、docs.anthropic.com）✅ | MT✅ MD✅ | 无 | 92 |
| 5 | what-is-model-distillation | 090 | 0.89% ✗ | ✓ | 1/5 | 62 ✅ | 145 ✅ | 2（arxiv.org、huggingface.co）✅ | **MT✗ MD✗** | 无 | 86 |
| 6 | ai-career-planning-guide | 091 | 1.07% ✅ | ✓ | 1/5 | 55 ✅ | 147 ✅ | 2（mohrss.gov.cn、moe.gov.cn）✅ | **MT✗ MD✗** | 无 | 88 |
| 7 | ai-deepfake-scam-protection | 096 | 0.92% ⚠️ | ✓ | 1/5 | 55 ✅ | 147 ✅ | 2（mps.gov.cn、cac.gov.cn）✅ | MT✅ **MD✗** | 无 | 89 |
| 8 | ai-content-labeling-rules | 098 | 0.89% ✗ | ✓ | 1/5 | 55 ✅ | 148 ✅ | 2（gov.cn 全文✅、cac.gov.cn✅）✅ | **MT✗ MD✗** | 无 | 86 |
| 9 | should-students-use-ai | 099 | 0.97% ⚠️ | ✓ | 1/5 | 57 ✅ | 155 ✅ | 2（moe.gov.cn、cac.gov.cn）✅ | **MT✗ MD✗** | 无 | 87 |
| 10 | ai-beginner-learning-path | 100 | 1.00% ✅ | ✓ | 1/5 | 53 ✅ | 146 ✅ | 2（learn.microsoft.com、openai.com）✅ | MT✅ **MD✗** | 无 | 90 |

> 密度为规范化命中（大小写/空格归一）÷ 正文中文字数。目标 1–2%。✅≥1.00%，⚠️0.90–0.99%，✗<0.90%。
> 主词入 Meta：精确主词串是否出现在 MT/MD（规范化后）。✗ 表示语义相近但非精确串（详见 P1-1）。
> 内链 10/10 无断链；外链 10/10 全官方/权威且实测有效。

---

## 三、P0 / P1 / P2 问题清单

### P0 — 诚信红线（必须修复）✅ 本批 0 项

全批 grep「实测」「待核实」「TODO」「通义灵码」「上下文窗口」「SWE-bench」均 0 命中；what-is-ai-hallucination 禁词铁律达标（无「上下文窗口」「SWE-bench」，「记性空间」出现 2 次）。

### P1 — 建议修复（1 项，涉及 6 篇 Meta，不影响发布资格）

#### P1-1：6 篇 Meta Description / 4 篇 Meta Title 未含精确主词（收尾批从严项）

- **现状**：Meta 宽度全批合格，但精确主词串未入 Meta 的有：
  - **MT+MD 均缺**（4 篇）：what-is-model-distillation（主词「模型蒸馏是什么」，标题为「模型蒸馏**和量化**是什么」）、ai-career-planning-guide（「ai做职业规划」vs「AI 职业规划是什么」）、ai-content-labeling-rules（「ai生成内容标识」vs「AI 生成内容**要标识吗**」）、should-students-use-ai（「学生用ai的利弊」vs「学生该不该用 AI」）
  - **仅 MD 缺**（2 篇）：ai-deepfake-scam-protection（MD「AI 换脸和合成声音…」未含「ai换脸诈骗怎么防」）、ai-beginner-learning-path（MD「非技术人学 AI 第一课…」未含「ai入门怎么学」）
- **影响**：精确主词在 Title/Description 的缺失削弱 SERP 相关性信号；因均为语义相近的自然变体（问题式标题），实际影响有限。
- **修复**：见第四节 Meta 元素优化建议（替代表案已给出并校验宽度）。

### P2 — 可不处理（优化细节）

- **P2-1 密度系统性略低于理想 1%**：6/10 篇 <1.0%（distillation 0.89、labeling 0.89、expense 0.92、deepfake 0.92、students 0.97、local 0.99）。每篇在结论/提示词段自然 +1~2 次主词即可进入舒适区。
- **P2-2 H2 含主词均为 1/5**：最低要求满足（≥1），理想 2 未达；与第 9/10 批一致，非阻塞。
- **P2-3 ai-beginner-learning-path 第三步代码块缺引导句**：L44-49 的提示词块（"把下面这段话改写成…"）前面缺少「下面这段可以直接抄：」式引导句，且该处有连续两个空行（L43-44）。建议补一句引导，与其他文章格式对齐。
- **P2-4 外链数恰为 2 条/篇**：达标（批 10 标准 2+），无质量问题，可后续按主题补充。

---

## 四、Meta 元素优化建议

> 按「只给不合格项」原则：题宽 10/10、述宽 10/10 全部合格，**无需改宽度**。以下仅针对 P1-1 中「精确主词未入 Meta」的 6 篇给出替代表案（宽度均已校验在 52–64 / 145–162 区间内）。

| 文章 | 当前题宽/述宽 | 问题 | 推荐 Meta Title（题宽） | 推荐 Meta Description（述宽） |
|------|--------------|------|------------------------|------------------------------|
| what-is-model-distillation | 62/145 | MT、MD 均缺精确主词 | 「模型蒸馏是什么？量化又是啥？两个类比讲清 — Learntide」(52) | 「模型蒸馏是什么？是让大模型当老师教出个聪明的小模型；量化则是给模型减肥。本文用大白话讲清两者区别，以及和手机 AI、本地部署的关系，看完不再被术语吓住。」(149) |
| ai-career-planning-guide | 55/147 | MT、MD 均缺精确主词 | 「AI 做职业规划怎么做？三步法与交叉验证边界 — Learntide」(53) | 「用 AI 做职业规划不是算命，是把经历整理成结构化信息、帮你看选项的顾问。本文讲三步法、可复制提示词，以及必须用真实岗位交叉验证的边界，建议以官网为准。」(148) |
| ai-deepfake-scam-protection | 55/147 | 仅 MD 缺精确主词 | 不变（MT 已含「AI 换脸诈骗怎么防」）(55) | 「AI 换脸诈骗怎么防？看到脸、听到声音都不算证据。本文给三个可照做的验证动作：电话回拨、对暗号、转账前多核一步，以及被仿冒后怎么办，以警方官方发布为准。」(149) |
| ai-content-labeling-rules | 55/148 | MT、MD 均缺精确主词 | 「AI 生成内容标识怎么做？新规执行与自查清单 — Learntide」(53) | 「AI 生成内容标识，2025-09-01 起成为强制义务。本文讲显式/隐式标识区别、工具方平台和你的义务，以及普通人发布时怎么标才合规，具体执行以官方发布为准。」(145) |
| should-students-use-ai | 57/155 | MT、MD 均缺精确主词 | 「学生用 AI 的利弊：三个好处三个风险一个标准 — Learntide」(54) | 「学生用 AI 的利弊，关键看用来理解还是代替理解。本文给三个好处、三个风险、一个判断标准，以及给家长和老师的三句话，帮助把边界定清楚，以学校规定为准。」(146) |
| ai-beginner-learning-path | 53/146 | 仅 MD 缺精确主词 | 不变（MT 已含「AI 入门怎么学」）(53) | 「AI 入门怎么学？非技术人第一课不是学编程，是把 AI 用起来。本文给「先用→再问→后理解」三步路线、两条路选择判断，以及新手最容易踩的四个坑，帮你从零开始不绕路。」(155) |

> 说明：P1-1 为「从严」建议项。若维持现状，6 篇标题/描述仍为语义等价的问题式变体，可接受但不理想；采用上表任一组即可让精确主词进入 Meta。改后需重新构建。

---

## 五、精选摘要捕获机会

全批 10/10 均为「结论前置 + 直答段 + 关键要点」结构，精选摘要条件已具备，无需改动。重点机会：

| 文章 | 摘要类型 | 现状 | 优先级 |
|------|---------|------|--------|
| ai-expense-tracking-guide | HowTo/List | 首段直答 + 四步流程 + 可复制提示词 + 隐私红线清单 | 高 |
| ai-chart-generation-guide | HowTo | 首段直答 + 两步路线 + 五要素提示词 + 三步检查 | 高 |
| local-ai-model-setup | HowTo | 首段直答 + 显存判断 + 一条命令 + 三种方式 | 高 |
| what-is-ai-hallucination | Definition | 首段「模型生成…其实是编的」定义直答，定义类摘要机会极佳 | 高 |
| what-is-model-distillation | Definition | 首段「老师教学生/减肥」双定义直答 | 高 |
| ai-career-planning-guide | List | 首段边界直答 + 三步法 + 提示词 ×2 | 高 |
| ai-deepfake-scam-protection | HowTo/List | 首段三动作直答 + 给爸妈三句话块 | 高 |
| ai-content-labeling-rules | Explain/List | 首段强制义务直答 + 自查清单 + 官方全文 | 高 |
| should-students-use-ai | List | 首段判断标准直答 + 三好三坏 + 自查清单 | 高 |
| ai-beginner-learning-path | HowTo | 首段三步直答 + 避坑清单 + 7 天计划提示词 | 高 |

---

## 六、发布检查清单

### 收尾批整体状态

- [x] 主关键词在 H1 / 首 H2 — 10/10 ✅
- [x] 主关键词在前 100 字 — 10/10 ✅
- [x] 主关键词在 1+ 个 H2 标题 — 10/10 ✅（理想 2 仅 0 篇，P2-2）
- [ ] 关键词密度 ≥1.0%（1–2% 目标下限） — 4/10 ✅（6 篇偏低，P2-1）
- [x] 3–5+ 正文内链，无断链 — 10/10 ✅
- [x] 外链为官方/权威域名 — 10/10 ✅（DNS 全通过；gov.cn/cac.gov.cn/arxiv 已实测有效）
- [x] Meta Title 52–64 显示宽 — 10/10 ✅
- [x] Meta Description 145–162 显示宽 — 10/10 ✅
- [ ] 精确主词入 Meta Title/Description — MT 6/10、MD 4/10（P1-1，可选修复）
- [x] 正文字数达标（按 article_type 分档） — 10/10 ✅
- [x] 正确 H1/H2/H3 层级 — 10/10 ✅（H2 均 5 个，无跳级）
- [x] 结论有明确 CTA — 10/10 ✅
- [x] 诚信红线（无 P0） — 10/10 ✅
- [x] 禁词「实测/待核实/TODO/通义灵码」 — 10/10 ✅
- [x] what-is-ai-hallucination 禁词铁律（无「上下文窗口」「SWE-bench」） — ✅（用「记性空间」，0 命中）
- [x] 仿冒镜像未链入 — 10/10 ✅（grammarlycn.cn/runwaychina/kling-ai/suno-zh/sora2-ai/trustoken/chatgptcn 全批 0）
- [x] 法律话题软表述 + 法条数字准确 — ✅（deepfake「据公开报道」无编造数字；labeling 2025-09-01 与官方第十四条一致）
- [x] 无断链（站内） — 10/10 ✅
- [x] ID 与选题总表一致 — 10/10 ✅（076/079/080/083/090/091/096/098/099/100）

### 逐篇发布状态

| 文章 | 状态 |
|------|------|
| ai-expense-tracking-guide | ✅ 可发布（密度 0.92% 临界，P2） |
| ai-chart-generation-guide | ✅ 可发布 |
| local-ai-model-setup | ✅ 可发布（密度 0.99% 临界，P2） |
| what-is-ai-hallucination | ✅ 可发布 |
| what-is-model-distillation | ✅ 可发布（P1-1 建议 Meta 补主词；arxiv 论文外链 ✅） |
| ai-career-planning-guide | ✅ 可发布（P1-1 建议 Meta 补主词） |
| ai-deepfake-scam-protection | ✅ 可发布（P1-1 建议 MD 补主词；软表述 ✅） |
| ai-content-labeling-rules | ✅ 可发布（P1-1 建议 Meta 补主词；gov.cn 全文 ✅） |
| should-students-use-ai | ✅ 可发布（P1-1 建议 Meta 补主词） |
| ai-beginner-learning-path | ✅ 可发布（P1-1 建议 MD 补主词；P2-3 代码块引导句） |

---

## 七、发布建议

### 状态：✅ Ready to Publish（可选执行 P1-1 增强）

**理由**：收尾批 10 篇质量延续第 10 批水准且更干净——**0 个 P0**、禁词铁律全批达标、外链全官方无失效、仿冒镜像零链入、法律话题软表述到位、精选摘要结构全批优良、Meta 宽度全批合格。综合 89/100 ≥70，**判定合格**。

### 建议（可选，非阻塞）

| 问题 | 位置 | 预估 |
|------|------|------|
| P1-1 Meta 补精确主词（6 篇） | 对应 6 篇 frontmatter meta_title/meta_description | 每篇 2 分钟，共约 12 分钟 |
| P2-3 代码块补引导句 | ai-beginner-learning-path（L44-49） | 1 分钟 |
| P2-1 密度 +1~2 次主词 | 6 篇结论/提示词段 | 每篇 2 分钟 |

改后重新构建 + 跑 qa_check 确认 0 FAIL 即可。

---

## 附录 A：本批特别关注项核验

| 关注项 | 结论 |
|--------|------|
| what-is-ai-hallucination：禁词铁律（无「上下文窗口」「SWE-bench」） | ✅ 全篇 0 命中；用「记性空间」×2 替代；内链锚文本用「AI 的记性空间」 |
| what-is-ai-hallucination：与 055（avoid-ai-hallucination-tips）分工清晰 | ✅ 正文末明确「这篇负责让你看懂『为什么』」，防错步骤指向 055，无重叠 |
| what-is-model-distillation：外链含 arxiv.org Hinton 论文 | ✅ `https://arxiv.org/abs/1503.02531`（Distilling the Knowledge in a Neural Network）已实测有效 |
| ai-deepfake-scam-protection：案件数量软表述 | ✅ 「据公开报道已有多起冒充亲友、冒充领导要钱的案件」，无编造具体数字 |
| ai-deepfake-scam-protection：外链 mps.gov.cn / cac.gov.cn | ✅ 两条均官方且 DNS 通过 |
| ai-content-labeling-rules：2025-09-01 新规表述 | ✅ 与《标识办法》第十四条「本办法自 2025年9月1日起施行」一致 |
| ai-content-labeling-rules：gov.cn 官方全文外链 | ✅ `gov.cn/zhengce/zhengceku/202503/content_7014286.htm` 已实测有效，含全文 |
| ai-beginner-learning-path：全站收尾篇内链引导到支柱页 | ✅ 内链含 ai-learning-path-guide（支柱页），正文明确「具体的工具路线可参考…本篇讲心态和方法」 |
| ai-beginner-learning-path：与 ai-learning-path-guide 区分 | ✅ 定位清晰（本篇=入门心态与三步法；支柱页=工具路线），无重复 |

## 附录 B：外链域名核验明细（收尾批 20 条）

| 域名 | 文章 | 性质 | 状态 |
|------|------|------|------|
| pay.weixin.qq.com | expense | 官方 | ✅ DNS 通过 |
| www.feidee.com | expense | 官方（随手记） | ✅ DNS 通过 |
| support.microsoft.com/zh-cn/excel | chart | 官方 | ✅ DNS 通过 |
| ai.wps.cn | chart | 官方 | ✅ DNS 通过 |
| ollama.com | local-ai | 官方 | ✅ DNS 通过 |
| github.com/ollama/ollama | local-ai | 官方仓库 | ✅ DNS 通过 |
| platform.openai.com/docs | hallucination | 官方 | ✅ DNS 通过 |
| docs.anthropic.com | hallucination | 官方 | ✅ DNS 通过 |
| arxiv.org/abs/1503.02531 | distillation | 权威论文 | ✅ 实测有效（Hinton 蒸馏论文） |
| huggingface.co/docs | distillation | 官方 | ✅ DNS 通过 |
| www.mohrss.gov.cn | career | 政务权威 | ✅ DNS 通过 |
| www.moe.gov.cn | career / students | 政务权威 | ✅ DNS 通过 |
| www.mps.gov.cn | deepfake | 政务权威 | ✅ DNS 通过 |
| www.cac.gov.cn | deepfake / labeling / students | 政务权威 | ✅ DNS 通过 |
| www.gov.cn（标识办法全文） | labeling | 政务权威 | ✅ 实测有效（含第十四条 2025-09-01） |
| learn.microsoft.com/zh-cn/training | beginner | 官方 | ✅ DNS 通过 |
| openai.com | beginner | 官方 | ✅ DNS 通过 |

---

*报告生成：2026-08-06 CST | 审计工具：seo-optimizer-4 人工审计 + 量化脚本（规范化密度/前100字/H2/Meta宽度/链接/红线全量扫描，drafts 与渲染 HTML 双重核验）+ DNS/WebFetch 外链实测*
