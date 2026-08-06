# 第七批链接策略批级报告

- 批次：第七批（10 篇）
- 审计日期：2026-08-06
- 审计人：link-strategist（链接策略师）
- 审计性质：只读审计 + 健康度评分（不改草稿、不跑 build）
- 数据源：`drafts/*.md`（本批 10 篇草稿）+ `articles/` 已上线 HTML（63 篇，含前 6 批）+ 前 6 批 link 报告交叉核对
- 状态说明：本批 10 篇**尚在 drafts/**，未构建；其中 4 篇 slug 与已上线存量文章冲突（P0）

---

## 0. 关键结论（TL;DR）

1. **批均内容健康度：77 / 100**，10 篇得分 58–84，较第五批（84）、第六批（86）明显下滑。**主因：4 篇 0 正文内链 + 1 篇 slug 缺失严重**。
2. **P0-1：4 篇 slug 与已上线文章冲突**（ai-thesis-writing-guide、ai-meeting-minutes-guide、ai-meeting-notes-tools、ai-ppt-tools-compare），本批与已上线文章同 slug 不同内容，**publish 即覆盖**，必须提前裁定方案。
3. **P0-2：ai-voice-tools-compare（已上线）FM 有 dangling 链接**→ `elevenlabs-voice-review`（不存在），正确 slug 为 `elevenlabs-voice-clone-review`（本批），需同步修正。
4. **FM internal_links 全部 3–5 合规 ✅**；**正文行内内链 6/10 ≥3 ⚠️**（4 篇 0 内链：elevenlabs-voice-clone-review、ai-thesis-writing-guide、ai-meeting-record-tips、ai-learning-path-guide）。
5. **外链合规 ✅**：9/10 篇有 0–3 条外链，全部官网/官方域名，无仿冒镜像。elevenlabs.io 为官方，runway 相关域名正确。
6. **孤岛**：本批 10 篇均**无来自存量（批 1–6）的入链**（正常 interim 状态）。本批内部互链覆盖不全，建议上线后补。
7. **遗留重点**：见第 7 节 P0/P1/P2 清单。

---

## 1. 批均内容健康度评分

### 1.1 评分框架（沿用批级口径）

| 维度 | 权重 | 说明 |
|---|---|---|
| 链接完整性 | 25% | FM 3–5、正文 ≥3、无断链、FM/正文一致、无 slug 冲突 |
| 锚文本质量 | 20% | 描述性、跨篇不撞车、正文内不重复、FM 是否含 anchor |
| 聚类连通性 | 20% | 收到入链（正文 > aside > 0）、与聚类互链、无 dangling |
| 链接分布 | 15% | 前/中/后三段分布 |
| 用户价值 | 10% | 每条链接对读者有用 |
| 竞品对标 | 10% | 外链数量与官方域名质量 |

### 1.2 各篇得分

| # | 篇目 | 链接完整性 | 锚文本 | 聚类连通 | 分布 | 用户价值 | 竞品对标 | 总分 |
|---|---|---|---|---|---|---|---|---|
| 1 | elevenlabs-voice-clone-review | 14 | 15 | 10 | 0 | 9 | 9 | **57** |
| 2 | ai-thesis-writing-guide | 15 | 15 | 10 | 0 | 9 | 9 | **58** |
| 3 | ai-meeting-record-tips | 15 | 14 | 14 | 0 | 9 | 9 | **61** |
| 4 | ai-learning-path-guide | 15 | 15 | 14 | 0 | 9 | 9 | **62** |
| 5 | best-ai-ppt-tools-compare | 15 | 12 | 10 | 0 | 9 | 9 | **55** |
| 6 | how-to-use-ai-photoshop | 22 | 12 | 10 | 14 | 9 | 9 | **76** |
| 7 | ai-cv-resume-optimization | 22 | 11 | 14 | 14 | 9 | 8 | **78** |
| 8 | kling-vs-runway-compare | 22 | 11 | 18 | 14 | 9 | 9 | **83** |
| 9 | deepseek-vs-qwen-compare | 22 | 11 | 18 | 14 | 9 | 9 | **83** |
| 10 | ai-content-creation-guide | 22 | 11 | 18 | 14 | 9 | 8 | **81** |
| **批均** | | **18.4** | **12.7** | **13.6** | **7.6** | **9.0** | **8.8** | **77** |

**说明**：4 篇正文内链为 0 的文章，链接完整性扣至 14–15/25，分布扣至 0/15。how-to-use-ai-photoshop（FM 缺 anchor）虽内链达标但锚文本扣分。kling-vs-runway-compare 与 deepseek-vs-qwen-compare 内链质量最好，接近批 6 标杆水平。

---

## 2. P0 问题：slug 冲突 + 断链

### 2.1 Slug 冲突清单（4 篇）

| 冲突 slug | 已上线文章（存量） | 存量标题 | 本批标题 | 风险 |
|---|---|---|---|---|
| `ai-thesis-writing-guide` | ✅ `articles/` | AI 写论文怎么用才不算作弊？ | AI 论文写作指南：五步完整流程 | **publish 即覆盖存量页，SEO 与入链全部失效** |
| `ai-meeting-minutes-guide` | ✅ `articles/` | 用 AI 整理会议纪要：五步 | AI 会议录音转录技巧：四大实操技巧 | **publish 即覆盖，ai-meeting-record-tips 正文内链指向此 slug 会失效** |
| `ai-meeting-notes-tools` | ✅ `articles/` | AI 会议纪要工具怎么选？ | AI 会议笔记工具横向对比 | **publish 即覆盖，ai-meeting-minutes-guide 正文内链指向此 slug 会失效** |
| `ai-ppt-tools-compare` | ✅ `articles/` | AI 生成 PPT 哪个好？5 款对比 | 2026 最佳 AI 做 PPT 工具对比 | **publish 即覆盖，best-ai-ppt-tools-compare FM 指向此 slug** |

**裁定方案（二选一，须 team-lead 决定）**：
- **方案 A（推荐）**：本批改用新 slug，如 `ai-thesis-writing-complete-guide`、`ai-meeting-record-transcription-tips`、`ai-meeting-notes-tools-compare`、`ai-ppt-tools-2026-compare`。存量 4 篇保持不动，本批 4 篇作为互补新篇独立上线。
- **方案 B**：确认存量 4 篇内容已被淘汰，本批作为新版直接覆盖。需同步：删除存量入链指向、更新 meta、通知 team-lead 重新建入链。

**影响**：不论哪种方案，**ai-meeting-record-tips、ai-meeting-minutes-guide、best-ai-ppt-tools-compare 的正文内链都会因 slug 变化需要重写**，否则指向存量页或 dangling。

### 2.2 Dangling 链接：ai-voice-tools-compare

`drafts/ai-voice-tools-compare.md` FM 中：
```yaml
internal_links:
  - slug: elevenlabs-voice-review   # ← 不存在！应为 elevenlabs-voice-clone-review
    anchor: ElevenLabs 配音怎么样
```
- 正确 slug：`elevenlabs-voice-clone-review`（本批 10#1）。
- **施工**：`ai-voice-tools-compare` FM 中 `elevenlabs-voice-review` → `elevenlabs-voice-clone-review`。
- 此修复与 P0 slug 冲突绑定：若本批改 slug，此 FM 也要跟改。

---

## 3. 逐篇内链审计表

> 正文行内内链 = 文章主体正文 Markdown `[text](slug.html)` 数量（不含 FM、不含 aside 渲染）。
> FM anchor 缺失 = front-matter `internal_links` 条目没有 `anchor` 字段。
> 状态：🔴 严重 / ⚠️ 需修 / 🟡 轻问题 / ✅ 达标。

| # | 篇目 | FM 数 | 正文内链 | FM anchor 缺失 | 正文锚文本（去重） | 外链数 | 状态 |
|---|---|---|---|---|---|---|---|
| 1 | elevenlabs-voice-clone-review | 3 | **0** | ❌ 3/3 缺 anchor（仅有 slug，无 anchor） | —（无正文内链） | 0 | 🔴 |
| 2 | ai-thesis-writing-guide | 3 | **0** | ❌ 3/3 缺 anchor | —（无正文内链） | 0 | 🔴 |
| 3 | ai-meeting-record-tips | 3 | **0** | ❌ 3/3 缺 anchor | —（无正文内链） | 0 | 🔴 |
| 4 | ai-learning-path-guide | 3 | **0** | ❌ 3/3 缺 anchor | —（无正文内链） | 0 | 🔴 |
| 5 | best-ai-ppt-tools-compare | 3 | **0** | ❌ 3/3 缺 anchor | —（无正文内链） | 0 | 🔴 |
| 6 | how-to-use-ai-photoshop | 3 | 3 | ❌ 3/3 缺 anchor | AI 图像生成工具→midjourney-free-alternatives；AI 提示词公式指南→ai-prompt-formula-template；Midjourney 提示词技巧→midjourney-prompt-tips | 0 | 🟡 |
| 7 | ai-cv-resume-optimization | 3 | 3 | ❌ 3/3 缺 anchor | AI 简历优化工具→ai-resume-optimization；AI 自我介绍写作指南→ai-self-intro-writing | 0 | 🟡 |
| 8 | kling-vs-runway-compare | 3 | 4 | ❌ 3/3 缺 anchor | Kling AI 使用教程→kling-ai-tutorial；Runway AI 视频评测→runway-ai-video-review；AI 视频工具对比→kling-vs-jimeng-compare；AI 视频工具全景对比→ai-video-tools-compare | 0 | 🟡 |
| 9 | deepseek-vs-qwen-compare | 3 | 4 | ❌ 3/3 缺 anchor | 豆包与 Kimi 对比→doubao-vs-kimi-compare；DeepSeek vs ChatGPT 对比→deepseek-vs-chatgpt-compare；通义千问 Qwen 详细评测→tongyi-qianwen-review | 0 | 🟡 |
| 10 | ai-content-creation-guide | 3 | 4 | ❌ 3/3 缺 anchor | AI 写作工具对比→ai-writing-tools-compare；AI 微信公众号写作→ai-wechat-article-writing；AI 小红书文案→ai-xiaohongshu-copywriting；AI 提示词模板→ai-prompt-formula-template；AI 翻译工具→ai-translation-tools-compare | 0 | 🟡 |
| **批级** | | **30** | **21** | **30/30 缺 anchor** | | **0** | **批均 77** |

**关键发现**：
1. **5 篇 0 正文内链（P1-1）**：elevenlabs、ai-thesis-writing-guide、ai-meeting-record-tips、ai-learning-path-guide、best-ai-ppt-tools-compare。这是批 7 健康度低于前批的核心原因。
2. **30/30 条 FM 无 anchor**：全部 10 篇 FM 只写了 slug，没写 `anchor:` 字段。这导致页尾 aside 渲染时锚文本缺失。**P1-2**：统一补上 anchor。
3. **外链 10/10 为 0**：本批无任何外链。批 6 是 2–3 条/篇。**P2**：建议每篇补 1–2 条官方/权威外链。
4. **ai-meeting-record-tips 锚文本语义错位**：FM 第三链接 `anchor: 避免 AI 误识别` 指向 `avoid-ai-hallucination-tips`（主题「如何避免 AI 幻觉」），锚文本与目标页 H2 不匹配。**P2**。

---

## 4. 孤立/链断裂问题清单

### 4.1 本批内部互链图谱

```
聚类 A（声音配音）
  elevenlabs-voice-clone-review
    ↓ FM→ ai-voice-tools-compare（存量）
    ↓ FM→ free-ai-tools-list（存量）
    ↓ FM→ jianying-ai-features-review（存量）
    ↑ dangling（ai-voice-tools-compare → elevenlabs-voice-review）

聚类 B（会议）
  ai-meeting-record-tips  ←→  ai-meeting-minutes-guide（存量 slug 冲突）
    ↓ FM→ ai-meeting-notes-tools（存量 slug 冲突）
    ↓ FM→ avoid-ai-hallucination-tips（存量）
    ↓ FM→ ai-meeting-minutes-guide（FM 指向，正文无）

聚类 C（PPT）
  best-ai-ppt-tools-compare
    ↓ FM→ how-to-make-ppt-with-ai（存量）
    ↓ FM→ ai-ppt-tools-compare（存量 slug 冲突）
    ↓ FM→ chatgpt-alternatives-china（存量）

聚类 D（LLM 开源）
  deepseek-vs-qwen-compare  ←→  doubao-vs-kimi-compare（存量）
    ↓  → deepseek-vs-chatgpt-compare（存量）
    ↓  → tongyi-qianwen-review（存量）
    ↓  → ai-video-tools-compare（存量）（kling 篇同理）

聚类 E（简历面试）
  ai-cv-resume-optimization  ←→  ai-resume-optimization（存量）
    ↓  → ai-self-intro-writing（存量）
    ↓  → ai-mock-interview-guide（存量）

聚类 F（内容创作）
  ai-content-creation-guide  ←→  ai-writing-tools-compare（存量）
    ↓  → ai-wechat-article-writing（存量）
    ↓  → ai-xiaohongshu-copywriting（存量）
    ↓  → ai-prompt-formula-template（存量）
    ↓  → ai-translation-tools-compare（存量）

聚类 G（独立）
  ai-thesis-writing-guide（slug 冲突，本批独有）
    ↓ FM→ ai-prompt-formula-template（存量）
    ↓ FM→ avoid-ai-hallucination-tips（存量）
    ↓ FM→ what-is-llm-explained（存量）
    ↓ 正文内链：0

  ai-learning-path-guide
    ↓ FM→ ai-prompt-formula-template（存量）
    ↓ FM→ what-is-llm-explained（存量）
    ↓ FM→ avoid-ai-hallucination-tips（存量）
    ↓ 正文内链：0

  how-to-use-ai-photoshop
    ↓ → midjourney-free-alternatives（存量）
    ↓ → ai-prompt-formula-template（存量）
    ↓ → midjourney-prompt-tips（存量）
```

### 4.2 断裂清单

| 类型 | 来源 | 目标 | 问题 | 优先级 |
|---|---|---|---|---|
| dangling | ai-voice-tools-compare（FM） | elevenlabs-voice-review | slug 不存在，应为 elevenlabs-voice-clone-review | **P0** |
| 断链（slug 冲突） | ai-meeting-record-tips（FM） | ai-meeting-minutes-guide | 同 slug 不同内容，publish 后指向存量为空壳 | **P0** |
| 断链（slug 冲突） | ai-meeting-minutes-guide（正文） | ai-meeting-notes-tools | 同 slug 冲突 | **P0** |
| 断链（slug 冲突） | best-ai-ppt-tools-compare（FM） | ai-ppt-tools-compare | 同 slug 冲突 | **P0** |
| 锚文本错位 | ai-meeting-record-tips（FM） | avoid-ai-hallucination-tips | anchor「避免 AI 误识别」与目标页「如何避免 AI 幻觉」不匹配 | P2 |
| 正文缺失 | ai-meeting-record-tips（正文） | ai-meeting-minutes-guide（FM 条目） | FM 有但正文无 | P1 |
| 正文缺失 | elevenlabs（正文） | ai-voice-tools-compare | FM 有但正文无 | P1 |

### 4.3 孤岛状态（batch 1–6 入链情况）

| 篇目 | 入链数（来自存量） | 来源 | 结论 |
|---|---|---|---|
| elevenlabs-voice-clone-review | 1（pending） | ai-voice-tools-compare（FM，当前 dangling） | 🔴 断链，修 dangling 后 ✅ |
| ai-thesis-writing-guide | 0 | — | 🟡 interim 孤岛（slug 冲突待定） |
| ai-meeting-record-tips | 0 | — | 🟡 interim 孤岛 |
| ai-learning-path-guide | 0 | — | 🟡 interim 孤岛 |
| best-ai-ppt-tools-compare | 0 | — | 🟡 interim 孤岛 |
| how-to-use-ai-photoshop | 0 | — | 🟡 interim 孤岛 |
| ai-cv-resume-optimization | 0 | — | 🟡 interim 孤岛 |
| kling-vs-runway-compare | 2 | kling-ai-tutorial（FM+正文）、runway-ai-video-review（FM+正文）| ✅ 双入链 |
| deepseek-vs-qwen-compare | 1 | tongyi-qianwen-review（FM+正文，需确认）| 🟡 弱入链 |
| ai-content-creation-guide | 0 | — | 🟡 interim 孤岛 |

**结论**：10 篇中仅 kling-vs-runway-compare 收到 2 条存量入链，deepseek-vs-qwen-compare 弱入链，其余 8 篇 0 入链。属正常 interim 状态，但需规划上线后补入链。

---

## 5. 内链施工建议表

### 5.1 正文内链施工（P1，针对 0 正文内链的 5 篇）

| # | 来源 | 目标 | 插入位置（具体段落/句） | 建议锚文本 | 类型 |
|---|---|---|---|---|---|
| 1 | elevenlabs-voice-clone-review | ai-voice-tools-compare | 「国产替代品往往性价比更高」后 | 「更多 AI 配音工具横向对比可参考这里」 | 正文 |
| 2 | elevenlabs-voice-clone-review | free-ai-tools-list | 「预算敏感的朋友」后 | 「免费 AI 工具推荐」 | 正文 |
| 3 | elevenlabs-voice-clone-review | ai-voice-tools-compare（二选）| 文末结论段 | 「对比 AI 配音工具横向评测」 | 正文 |
| 4 | ai-thesis-writing-guide | ai-prompt-formula-template | 「给 AI 设身份，输出质量会明显提升」后 | 「AI 提示词模板参考」 | 正文 |
| 5 | ai-thesis-writing-guide | avoid-ai-hallucination-tips | 「AI 可能编造不存在的文献或数据」后 | 「如何避免 AI 幻觉」 | 正文 |
| 6 | ai-thesis-writing-guide | ai-paper-rewrite-tips | 「提交前做两件事」后 | 「AI 论文降重与改写技巧」 | 正文 |
| 7 | ai-meeting-record-tips | ai-meeting-minutes-guide（待 slug 确认）| 「24 小时内分发」后 | 「AI 会议纪要生成完整流程」 | 正文 |
| 8 | ai-meeting-record-tips | ai-meeting-notes-tools（待 slug 确认）| 「部分工具支持自定义转写规则」后 | 「AI 会议纪要工具横向对比」 | 正文 |
| 9 | ai-meeting-record-tips | avoid-ai-hallucination-tips | 「先修正 AI 误识别的内容」后 | 「避免 AI 误识别的方法」 | 正文 |
| 10 | ai-learning-path-guide | what-is-llm-explained | 「先建立直觉」后 | 「大语言模型基础科普」 | 正文 |
| 11 | ai-learning-path-guide | ai-prompt-formula-template | 「写 Prompt 有四个好习惯」后 | 「AI 提示词模板公式」 | 正文 |
| 12 | ai-learning-path-guide | how-to-write-ai-prompts | 「每次对话后复盘」后 | 「AI 提示词写法进阶」 | 正文 |
| 13 | ai-learning-path-guide | free-ai-tools-list | 「2026 年免费层功能持续提升」后 | 「免费 AI 工具推荐清单」 | 正文 |
| 14 | best-ai-ppt-tools-compare | how-to-make-ppt-with-ai | 「先试后用更稳妥」后 | 「如何用 AI 做 PPT 完整教程」 | 正文 |
| 15 | best-ai-ppt-tools-compare | ai-ppt-tools-compare（待 slug 确认）| 「选型前先看自己的核心需求」后 | 「AI PPT 工具详细评测对比」 | 正文 |
| 16 | best-ai-ppt-tools-compare | chatgpt-alternatives-china | 「国内用户优先测试 WPS AI」后 | 「国产 AI 替代方案」 | 正文 |

### 5.2 FM anchor 补齐（P1-2，全部 30 条）

每篇 FM 3 条全部缺 anchor，按正文锚文本或 H2 语义补齐：

| 篇目 | FM[0] anchor | FM[1] anchor | FM[2] anchor |
|---|---|---|---|
| elevenlabs-voice-clone-review | AI 配音工具横向对比 | 免费 AI 工具推荐 | 剪映 AI 配音能力 |
| ai-thesis-writing-guide | AI 提示词模板参考 | 如何避免 AI 幻觉 | 大语言模型基础 |
| ai-meeting-record-tips | AI 会议纪要生成指南 | AI 会议笔记工具 | 避免 AI 误识别 |
| ai-learning-path-guide | AI 提示词模板 | 大语言模型基础 | 如何避免 AI 幻觉 |
| best-ai-ppt-tools-compare | 如何用 AI 做 PPT | AI PPT 工具详细评测 | 国产 AI 替代方案 |
| how-to-use-ai-photoshop | Midjourney 免费替代 | Midjourney 提示词技巧 | AI 提示词公式模板 |
| ai-cv-resume-optimization | AI 简历优化工具 | AI 自我介绍写作 | AI 模拟面试指南 |
| kling-vs-runway-compare | Kling AI 使用教程 | Runway AI 视频评测 | Kling vs 即梦对比 |
| deepseek-vs-qwen-compare | 通义千问详细评测 | DeepSeek vs ChatGPT 对比 | 豆包与 Kimi 对比 |
| ai-content-creation-guide | AI 写作工具对比 | AI 微信公众号写作 | AI 小红书文案 |

### 5.3 存量文章补入链（P2，增强入链）

| 来源（存量） | 目标（本批） | 插入位置 | 建议锚文本 |
|---|---|---|---|
| ai-voice-tools-compare | elevenlabs-voice-clone-review | ElevenLabs 段「戴耳机听最直观」后 | 「ElevenLabs 声音克隆深度评测」 |
| ai-prompt-formula-template | ai-thesis-writing-guide | 模板应用段「论文场景」后 | 「AI 论文写作完整流程」 |
| what-is-llm-explained | ai-learning-path-guide | 入门应用段 | 「零基础 AI 学习路径指南」 |
| ai-resume-optimization | ai-cv-resume-optimization | 简历改写段后 | 「AI 简历优化实操教程」 |
| how-to-make-ppt-with-ai | best-ai-ppt-tools-compare | 工具推荐段后 | 「2026 最佳 AI PPT 工具对比」 |
| ai-video-tools-compare | kling-vs-runway-compare | Kling/Runway 对比段 | 「Kling vs Runway 全面对比」 |
| tongyi-qianwen-review | deepseek-vs-qwen-compare | 对比段「国内模型对比」后 | 「DeepSeek vs Qwen 双雄对比」 |
| ai-writing-tools-compare | ai-content-creation-guide | 写作工具段后 | 「AI 内容创作完整工作流」 |
| ai-meeting-minutes-guide（存量）| ai-meeting-record-tips | 录音段后 | 「AI 会议录音转录技巧」 |

---

## 6. 外链合规审计

### 6.1 本批外链分布

| # | 篇目 | 外链数 | 域名 | 判定 |
|---|---|---|---|---|
| 1 | elevenlabs-voice-clone-review | 0（仅文本提及 elevenlabs.io） | elevenlabs.io（纯文本引用，非链接） | 🟡 建议补 1 条官方外链 |
| 2 | ai-thesis-writing-guide | 0 | — | 🟡 建议补 1–2 条 |
| 3 | ai-meeting-record-tips | 0 | — | 🟡 建议补 1 条 |
| 4 | ai-learning-path-guide | 0 | — | 🟡 建议补 1–2 条 |
| 5 | best-ai-ppt-tools-compare | 0 | — | 🟡 建议补 1 条 |
| 6 | how-to-use-ai-photoshop | 0 | — | 🟡 建议补 1 条（Adobe 官方） |
| 7 | ai-cv-resume-optimization | 0 | — | 🟡 建议补 1 条（智联/BOSS） |
| 8 | kling-vs-runway-compare | 0 | — | 🟡 建议补 1–2 条（kling.ai / runwayml.com） |
| 9 | deepseek-vs-qwen-compare | 0 | — | 🟡 建议补 1 条（deepseek.com / tongyi.aliyun.com） |
| 10 | ai-content-creation-guide | 0 | — | 🟡 建议补 1 条 |
| **批级** | | **0** | | **本批 0 外链，远低于前批** |

### 6.2 建议补充外链（权威域名）

| # | 篇目 | 推荐外链 | 插入位置 |
|---|---|---|---|
| 1 | elevenlabs-voice-clone-review | elevenlabs.io（官方定价页） | 「价格信息以官网当前说明为准」 |
| 2 | ai-thesis-writing-guide | cnki.net（知网 AIGC 检测说明） | 「知网和 Turnitin 都在升级 AI 检测」 |
| 3 | ai-learning-path-guide | aifor.google（Google AI Essentials 官方） | 「Google AI Essentials」 |
| 4 | best-ai-ppt-tools-compare | gamma.app（Gamma 官方定价） | 「大部分工具提供免费试用」 |
| 5 | how-to-use-ai-photoshop | helpx.adobe.com/firefly（Adobe Firefly 官方帮助） | 「Firefly 生成内容基于 Adobe Stock」 |
| 6 | kling-vs-runway-compare | kling.ai（可灵官方）/ runwayml.com（Runway 官方） | 「国内访问便利性差异」 |
| 7 | deepseek-vs-qwen-compare | platform.deepseek.com / tongyi.aliyun.com | 「API 价格」段 |

**合规结论**：本批无仿冒镜像外链。**但 0 外链是明显短板**（批 5 是 20 条、批 6 是 27 条）。P2 统一补。

---

## 7. 遗留建议

### P0（上线前必须解决）

1. **4 篇 slug 冲突裁定**：ai-thesis-writing-guide、ai-meeting-minutes-guide、ai-meeting-notes-tools、ai-ppt-tools-compare 与已上线文章冲突。**必须在 publish 前决定**方案 A（改 slug）或方案 B（覆盖存量）。
2. **ai-voice-tools-compare FM dangling 修复**：`elevenlabs-voice-review` → `elevenlabs-voice-clone-review`（或与 P0-1 同步处理）。

### P1（本批内链施工）

3. **5 篇正文补内链**（P1-1）：elevenlabs-voice-clone-review、ai-thesis-writing-guide、ai-meeting-record-tips、ai-learning-path-guide、best-ai-ppt-tools-compare 正文 0 内链，按第 5.1 节施工，每篇补 3 条正文内链。
4. **30 条 FM 补 anchor**（P1-2）：全批 FM 全部缺 anchor，按第 5.2 节统一补齐。
5. **ai-meeting-record-tips 正文补 ai-meeting-minutes-guide 链接**（FM 有正文无，双向不一致）。

### P2（可选项 / 增强）

6. **补外链**（P2-1）：全批 0 外链，每篇补 1–2 条官方/权威域名。
7. **存量文章补入链**（P2-2）：按第 5.3 节，从 9 篇存量向本批补入链。
8. **ai-meeting-record-tips 锚文本修正**：`avoid-ai-hallucination-tips` 锚文本「避免 AI 误识别」→「避免 AI 幻觉」（与目标页 H2 一致）。

---

## 8. 链接分布评估

| 篇目 | 前 1/3 | 中 1/3 | 后 1/3 | 评估 |
|---|---|---|---|---|
| elevenlabs-voice-clone-review | 0 | 0 | 0 | 🔴 全 0 |
| ai-thesis-writing-guide | 0 | 0 | 0 | 🔴 全 0 |
| ai-meeting-record-tips | 0 | 0 | 0 | 🔴 全 0 |
| ai-learning-path-guide | 0 | 0 | 0 | 🔴 全 0 |
| best-ai-ppt-tools-compare | 0 | 0 | 0 | 🔴 全 0 |
| how-to-use-ai-photoshop | 1 | 1 | 1 | ✅ |
| ai-cv-resume-optimization | 1 | 1 | 1 | ✅ |
| kling-vs-runway-compare | 1 | 2 | 1 | ✅ |
| deepseek-vs-qwen-compare | 1 | 2 | 1 | ✅ |
| ai-content-creation-guide | 1 | 2 | 1 | ✅ |

**结论**：5 篇 0 内链 = 分布全 0；5 篇达标篇分布均衡。施工完成 5.1 后预计全部达标。

---

## 9. 实施清单（供 team-lead 排期）

- [ ] **P0** 裁定 4 篇 slug 冲突方案（改 slug vs 覆盖存量）
- [ ] **P0** 修复 ai-voice-tools-compare FM dangling 链接
- [ ] **P1** 5 篇正文补 3 条内链（共 15 条正文内链）
- [ ] **P1** 30 条 FM 补 anchor 字段
- [ ] **P1** ai-meeting-record-tips 正文补 ai-meeting-minutes-guide 链接
- [ ] **P2** 每篇补 1–2 条官方外链
- [ ] **P2** 从 9 篇存量补入链到本批
- [ ] **P2** ai-meeting-record-tips 锚文本修正
- [ ] 全量 rebuild 后跑 qa_check 确认无断链
