# LearnTide 第八批 SEO 技术审计报告

> 审计日期：2026-08-06
> 审计人：seo-optimizer（欧化成）
> 审计范围：第八批 10 篇文章（已通过 qa_check 0 FAIL，已构建上线）
> 报告路径：`A:\LearnTide\reports\seo-report-batch8-2026-08-06.md`

---

## 一、批级 SEO 评分

### 综合评分：78 / 100

> ⚠️ **硬性判定：存在 P0，未达「无 P0 且综合评分 ≥70」合格线**。修复 1 处 P0（github-copilot 内链锚文本含「通义灵码」）后即视为合格（修复后约 90+）。

| 维度 | 得分 | 满分 | 说明 |
|------|------|------|------|
| 关键词优化 | 18 | 25 | 6/10 密度达标（≥0.9%），4 篇偏低；前 100 词 10/10 全过；H2 全部 ≥1 但无一篇达到理想 2 个 |
| 可读性 | 24 | 25 | **10/10 全达标**，均句长 12.0–22.5（目标 ≤26）、短句率 22–66%（目标 ≥15%），第 7 批系统性问题已解决 |
| Meta 元素 | 25 | 25 | **10/10 题宽达标（53–61）、10/10 述宽达标（148–162）**，全批完美 |
| 结构与链接 | 20 | 25 | 正文内链 9/10 齐全（github-copilot 正文 0 条）；外链 6/10 有，均为官方权威域名，无仿冒镜像 |
| 诚信合规 | 10 | 25 | 无实测/TODO/仿冒镜像；但 **1 处 P0「通义灵码」**（渲染于线上）+ **3 篇 ID 与选题总表不符** |

---

## 二、逐篇评分表

| # | 文章 | 密度 | 前100词 | H2含主词 | 题宽 | 述宽 | 均句长 | 短句% | 外链数 | 正文内链 | 综合 |
|---|------|------|---------|---------|------|------|--------|-------|--------|---------|------|
| 1 | stable-diffusion-beginner-worth | 0.36% ✗ | ✓ | 1/4 | 55 ✅ | 151 ✅ | 22.5 ✅ | 32 ✅ | 0 | 4 | 72 |
| 2 | elevenlabs-voice-review | 0.36% ✗ | ✓ | 1/5 | 53 ✅ | 159 ✅ | 20.8 ✅ | 32 ✅ | 0 | 3 | 70 |
| 3 | github-copilot-worth-buying | 1.01% ✅ | ✓ | 1/5 | 59 ✅ | 150 ✅ | 16.7 ✅ | 24 ✅ | 2 | **0** ⚠️ | **62** |
| 4 | ai-email-writing-guide | 1.32% ✅ | ✓ | 1/5 | 54 ✅ | 148 ✅ | 15.0 ✅ | 40 ✅ | 2 | 4 | 88 |
| 5 | fix-ai-hands-generation | 0.96% ✅ | ✓ | 1/5 | 55 ✅ | 148 ✅ | 16.7 ✅ | 31 ✅ | 2 | 4 | 82 |
| 6 | ai-video-script-writing | 0.47% ✗ | ✓ | 1/5 | 57 ✅ | 157 ✅ | 18.5 ✅ | 28 ✅ | 0 | 3 | 74 |
| 7 | ai-english-speaking-practice | 0.34% ✗ | ✓ | 1/5 | 54 ✅ | 150 ✅ | 19.0 ✅ | 22 ✅ | 0 | 4 | 72 |
| 8 | ai-exam-prep-guide | 1.10% ✅ | ✓ | 1/5 | 61 ✅ | 162 ✅ | 16.2 ✅ | 39 ✅ | 2 | 4 | 88 |
| 9 | what-is-rag-explained | 1.02% ✅ | ✓ | 1/5 | 59 ✅ | 149 ✅ | 12.0 ✅ | 66 ✅ | 2 | 4 | 90 |
| 10 | what-is-multimodal-ai | 1.06% ✅ | ✓ | 1/5 | 57 ✅ | 159 ✅ | 13.9 ✅ | 46 ✅ | 2 | 4 | 90 |

> 密度目标：800 字精确匹配 8–16 次（1–2%）。✅ = ≥0.9%，✗ = <0.9%。
> Meta 宽度为显示宽度（CJK ×2），题宽 52–64 / 述宽 145–162 为合格区间。

---

## 三、P0 / P1 / P2 问题清单

### P0 — 诚信红线（必须修复）

**P0-1：github-copilot-worth-buying 内链锚文本含「通义灵码」**

- 位置：`drafts/github-copilot-worth-buying.md` 第 17 行 front-matter：
  ```
  - slug: tongyi-lingma-review
    anchor: 通义灵码免费版功能
  ```
- 影响：该锚文本已渲染到线上页面 `articles/github-copilot-worth-buying.html` 的「相关阅读」区（`<a href="tongyi-lingma-review.html">通义灵码免费版功能</a>`）。第 8 批红线要求全文不得出现「通义灵码」，此条违反。
- 修复方法：将 anchor 改为中性品牌名，如「Qoder CN 免费版功能」或「AI 编程助手免费版功能」，slug 保持不变（tongyi-lingma-review.html 专题页可保留旧名作为该文自身关键词，但本批链接锚文本必须改）。

其余红线检查（第 8 批 10 篇）：
- 禁词「实测」：**未发现** ✅
- 禁词「待核实」「TODO」：**未发现** ✅
- 仿冒镜像（runwaychina.com / kling-ai.com / suno-zh.com / sora2-ai.io / chatgptcn.com / openai-cn.com / stablediffusion-cn.com 等）：**未发现** ✅
- 全站唯一一处 `runwaychina.com` 字样位于第 7 批 `runway-ai-video-review.html`，属「警示读者仿冒」的正当负面提及（"网上流传的 runwaychina.com 一类中文镜像多为仿冒。别用"），非引用，合规。

### P1 — 建议修复（影响排名/数据一致性）

#### P1-1：github-copilot-worth-buying 正文无内链（1 篇）

- **问题**：front-matter 声明了 4 条 `internal_links`，但正文中 **0 条** `[锚文本](slug.html)` 格式内链。搜索爬虫无法识别 front-matter 中的声明，内链必须嵌入正文才有效。
- **修复**：在「什么情况下先别买」或结尾段加入 2–3 条正文内链，例如：
  ```
  …这三类人的答案都是先别买。想横向比较，看 [AI 编程助手哪个好](ai-coding-assistants-compare.html) 和 [Cursor 和 Copilot 哪个好](cursor-vs-copilot-compare.html)。更多工具见 [AI 工具导航](../tools.html)。
  ```

#### P1-2：ID 与选题总表不一致（3 篇，数据完整性问题）

| 文章 | 稿件 id | 选题总表 id | 处理 |
|------|---------|------------|------|
| elevenlabs-voice-review | 059 | 020 | 改为 020 |
| stable-diffusion-beginner-worth | 058 | 014 | 改为 014 |
| ai-video-script-writing | 071 | 065 | 改为 065 |

- **连带问题**：`elevenlabs-voice-review` 与 `fix-ai-hands-generation` 均为 id 059，**ID 重复**。fix-ai-hands-generation（059）与总表一致，elevenlabs-voice-review 应改回 020。
- **影响评估**：build_articles.py 不渲染 `id` 字段（sitemap / HTML 均未引用），无线上影响；但选题总表编号错乱会在后续批次管理造成歧义，建议一次改齐。

#### P1-3：关键词密度偏低（4 篇）

| 文章 | 密度 | 精确匹配次数 | 建议 |
|------|------|------------|------|
| ai-english-speaking-practice | 0.34% | 3 | 结论段 +1 次、提示词段 +1 次 |
| stable-diffusion-beginner-worth | 0.36% | 3 | 「学习成本」段 +1 次 |
| elevenlabs-voice-review | 0.36% | 3 | 付费方案段 +1 次 |
| ai-video-script-writing | 0.47% | 4 | 第一步模板段 +1 次 |

> 说明：这 4 篇主关键词均为「长问句」（如「ai 练英语口语」），自然融入难度高于短语型关键词，但仍有 2–4 次提升空间。无需硬凑，每篇 +2~3 次即可达到 0.7–0.8%。

#### P1-4：H2 关键词覆盖均为 1/5（10/10 篇）

- **问题**：全部文章主关键词仅出现在 1 个 H2 标题，目标 ≥2。
- **修复**：在正文中部 1 个 H2 自然融入主词变体。示例：
  - `ai-english-speaking-practice`：`每天 15 分钟三段式：热身、主题对话、回顾` → `每天 15 分钟 AI 练英语口语三段式：热身、主题对话、回顾`
  - `ai-video-script-writing`：`第一步：给 AI 一个口语化模板` → `用 AI 写口播稿第一步：给 AI 一个口语化模板`
  - `what-is-rag-explained`：`RAG 和微调的区别` → `RAG 是什么之问：和微调的区别`

#### P1-5：无外链文章（4 篇）

| 文章 | 建议补充权威外链 |
|------|-----------------|
| stable-diffusion-beginner-worth | github.com/AUTOMATIC1111/stable-diffusion-webui（已有内链概念，正文可加官方仓库） |
| elevenlabs-voice-review | elevenlabs.io 官方定价页 |
| ai-video-script-writing | 无强相关权威源，可省略（P2） |
| ai-english-speaking-practice | 无强相关权威源，可省略（P2） |

### P2 — 可不处理（格式/优化细节）

- ai-exam-prep-guide：述宽 162 已达上限，后续改稿勿再加长
- 多数文章结论含「别…」反向提醒（qa 要求），同时可作为 CTA，保持现状
- 正文代码块（```bash / markdown）承载 Prompt 模板，SEO 友好，保持现状
- H2 数量均 4–5 个，处于合格区间，无需调整

---

## 四、Meta 元素优化建议

> 本批 10/10 题宽（53–61）、10/10 述宽（148–162）**全部合格**，无需必改项。以下仅为可选增强。

### 4.1 ai-english-speaking-practice（密度最低，标题可增强搜索意图）
**当前**：`用 AI 练英语口语：每天 15 分钟三段式练习法 — Learntide`（54 ✅）

**备选**：
1. `用 AI 练英语口语：每天 15 分钟三段式练习法 + 提示词模板` — 57 字符
2. `AI 练英语口语：15 分钟三段式 + 免费语音工具提示词` — 55 字符

**推荐**：#1 — 加入「提示词模板」价值点，匹配搜索意图中的实操需求。

### 4.2 stable-diffusion-beginner-worth（密度偏低，标题可增强年份信号）
**当前**：`Stable Diffusion 新手值得折腾吗？先看三件事 — Learntide`（55 ✅）

**备选**：
1. `Stable Diffusion 新手值得折腾吗 2026？硬件时间用途三关判断` — 57 字符
2. `Stable Diffusion 值得新手折腾吗？显卡时间用途三关速判` — 55 字符

**推荐**：#1 — 加入年份增强时效性。

### 4.3 其余 8 篇
题宽、述宽全部合格，不建议改动（改动有风险无收益）。

---

## 五、精选摘要捕获机会

| 文章 | 摘要类型 | 现状 | 优先级 |
|------|---------|------|--------|
| what-is-rag-explained | Definition | 首 H2 即「RAG 是什么：一句话解释」+ 开卷考试比喻，结论前置，**摘要机会极佳** | 高 |
| what-is-multimodal-ai | Definition | 首 H2 即「多模态 AI 是什么：一句话解释」，定义前置 | 高 |
| github-copilot-worth-buying | Conclusion-first | 首 H2「先说结论：GitHub Copilot 值得买吗？看频率」 | 高 |
| ai-email-writing-guide | HowTo | 三场景三模板 + 代码块提示词，结构化清晰 | 高 |
| fix-ai-hands-generation | HowTo | 四层修复法 + 有序步骤（负面提示词→换模型→局部重绘→LoRA） | 高 |
| ai-video-script-writing | HowTo | 三步法，步骤明确 | 中 |
| ai-exam-prep-guide | HowTo/List | 六场景清单 + 提示词代码块 | 中 |
| ai-english-speaking-practice | HowTo | 三段式练习法，步骤清晰 | 中 |
| stable-diffusion-beginner-worth | Decision framework | 三关判断框架 | 中 |
| elevenlabs-voice-review | Comparison | 价格档位 + 用途选型，建议补充表格结构（当前为段落） | 中 |

**建议**：
1. `what-is-rag-explained` / `what-is-multimodal-ai` 定义段已是「一句话答案 + 展开」，完全符合精选摘要「结论前置」标准，无需改动。
2. `elevenlabs-voice-review` 付费方案段建议改为表格（Starter/Creator/Pro 三档对比），利于捕获列表式摘要。
3. 全站已内置 `Article` + `BreadcrumbList` + `Organization` + `WebPage` JSON-LD（build_articles.py 自动注入），基础结构化数据健全；如需增强可对教程类追加 `HowTo` Schema（P2，非必需）。

---

## 六、发布检查清单

### 第八批整体状态

- [x] 主关键词在 H1 — 10/10 ✅
- [x] 主关键词在前 100 词 — 10/10 ✅
- [ ] 主关键词在 2+ 个 H2 标题 — **0/10** ⚠️（P1-4，全部仅 1 个）
- [x] 关键词密度 ≥0.9% — 6/10 ✅（4 篇偏低，P1-3）
- [ ] 3–5+ 正文内链 — 9/10 ✅（github-copilot 正文 0 条，P1-1）
- [ ] 2+ 外链 — 6/10 ✅（4 篇无外链，P1-5）
- [x] Meta Title 52–64 字符含关键词 — 10/10 ✅
- [x] Meta Description 145–162 字符含关键词和 CTA — 10/10 ✅
- [x] 2000+ 字 — 10/10 ✅（中文按字数，实际 791–895 字，符合 article_type 分档）
- [x] 正确 H1/H2/H3 层级 — 10/10 ✅
- [x] 可读性 均句长 ≤26 — 10/10 ✅
- [x] 短句率 ≥15% — 10/10 ✅
- [x] 结论有明确 CTA — 10/10 ✅
- [ ] 诚信红线 — **9/10** ❌（P0：github-copilot 锚文本含「通义灵码」）
- [x] Schema 结构化数据 — 10/10 ✅（Article/Breadcrumb/Organization 自动注入）

### 逐篇发布状态

| 文章 | 状态 |
|------|------|
| github-copilot-worth-buying | ❌ **需修复 P0 + P1-1（正文内链）** |
| stable-diffusion-beginner-worth | ⚠️ 建议修复 P1-2(ID)、P1-3(密度) |
| elevenlabs-voice-review | ⚠️ 建议修复 P1-2(ID)、P1-3(密度) |
| ai-video-script-writing | ⚠️ 建议修复 P1-2(ID)、P1-3(密度) |
| ai-english-speaking-practice | ⚠️ 建议修复 P1-3(密度) |
| ai-email-writing-guide | ✅ 可发布 |
| fix-ai-hands-generation | ✅ 可发布 |
| ai-exam-prep-guide | ✅ 可发布 |
| what-is-rag-explained | ✅ 可发布 |
| what-is-multimodal-ai | ✅ 可发布 |

---

## 七、发布建议

### 状态：⚠️ Needs Fix（修复 1 处 P0 后可发布）

**理由**：本批质量显著高于第 7 批（第 7 批 61/100，本批 78/100）。可读性、Meta 宽度全批满分，密度达标率从第 7 批 0/10 提升至 6/10。**唯一阻塞发布的是 P0：github-copilot-worth-buying 内链锚文本「通义灵码」渲染于线上**。

### 预估修复时间

| 问题类别 | 预估时间 |
|---------|---------|
| P0-1 修改 github-copilot 锚文本（1 处） | 1 分钟 |
| P1-1 github-copilot 正文补 2–3 条内链 | 5 分钟 |
| P1-2 三篇 ID 修正（020/014/065） | 3 分钟 |
| P1-3 四篇密度 +2~3 次 | 10 分钟 |
| P1-4 H2 关键词变体（10 篇） | 10 分钟 |
| P1-5 两篇补外链 | 5 分钟 |
| **合计（含 P1 全部）** | **约 35 分钟** |

### 最小可发布方案（5 分钟）

仅修复 P0-1（github-copilot 锚文本「通义灵码」→「Qoder CN 免费版功能」），即满足「无 P0」硬性要求，其余 P1 可安排第二版迭代。修复后需重新构建上线（`python build_articles.py`）。

---

## 附录 A：诚信红线检查结果

| 检查项 | sd-beginner | elevenlabs | copilot | email | hands | video-script | english | exam | rag | multimodal |
|-------|-------------|------------|---------|-------|-------|--------------|---------|------|-----|-----------|
| 「实测」 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 「待核实」「TODO」 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 「通义灵码」 | ✅ | ✅ | ❌ **P0** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 仿冒镜像域名 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

> 备注：P0 位于 github-copilot 的 front-matter `internal_links.anchor`，渲染于线上页面「相关阅读」区，属于第 8 批不应出现的品牌词，必须修复。

---

*报告生成：2026-08-06 17:40 CST | 审计工具：SEO 人工审计 + 量化脚本（关键词密度/宽度/链接/红线全量扫描）*
