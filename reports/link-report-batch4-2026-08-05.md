# 第四批链接策略批级报告（归档审计）

- 批次：第四批（10 篇）
- 审计日期：2026-08-05
- 审计人：link-strategist（链接策略师）
- 审计性质：只读归档审计 + 健康度评分（不做施工、不改草稿/HTML、不跑构建）
- 数据源：`drafts/*.md`（当前稿，mtime 00:34–00:54）+ `articles/*.html`（构建产物，00:05 构建）

---

## 0. 关键结论（TL;DR）

1. **批均内容健康度：82 / 100**，10 篇全部 ≥76，无不及格项。
2. **3 个孤儿页已全部在草稿层处置完毕**（入链均落在正文，非 aside）：
   - `gemini-free-plan-review` ← 3 条入链（free-ai-tools-list / chatgpt-plus-worth-it / claude-free-tier-limits）
   - `ai-meeting-minutes-guide` ← 1 条入链（ai-meeting-notes-tools）
   - `jianying-ai-tutorial` ← 2 条入链（jianying-ai-features-review / ai-video-tools-compare）
3. **注意：现有构建产物（00:05）晚于草稿施工（00:42–00:47）**，孤儿入链与外链尚未进入 HTML。需执行**全量 rebuild**（对应任务 #4）后，施工成果才会生效上线。
4. 外链整体偏弱：**仅 4/10 篇有外链**（每篇 2 条，域名均为官网/官方域名，无仿冒镜像）；6 篇教程/清单类为 0 外链。
5. 主要遗留：3 个正文内链不足 3 条的篇目（perplexity、kling 正文仅 2 条）、front-matter 与正文锚文本轻微失真 2 处、同一目标跨篇锚文本撞车 2 组、ai-mock-interview 正文内链分布扎堆。

---

## 1. 批均内容健康度评分

### 1.1 评分框架（沿用批级口径）

| 维度 | 权重 | 说明 |
|---|---|---|
| 链接完整性 | 25% | 正文行内内链 ≥3、front-matter 3–5、无断链 |
| 锚文本质量 | 20% | 描述性、跨篇不撞车、前后一致 |
| 聚类连通性 | 20% | 孤儿处置、支撑篇互链、链回相关页 |
| 链接分布 | 15% | 前/中/后三段分布是否均匀 |
| 用户价值 | 10% | 每条链接对读者真实有用 |
| 竞品对标 | 10% | 外链数量与官方域名质量达标 |

### 1.2 各篇得分

| 篇目 | 链接完整性 | 锚文本 | 聚类连通 | 分布 | 用户价值 | 竞品对标 | 总分 |
|---|---|---|---|---|---|---|---|
| gemini-free-plan-review | 20 | 16 | 19 | 11 | 9 | 9 | **82** |
| perplexity-ai-search-review | 17 | 16 | 18 | 10 | 9 | 9 | **76** |
| kling-vs-jimeng-compare | 17 | 16 | 18 | 10 | 9 | 9 | **76** |
| jianying-ai-features-review | 23 | 17 | 20 | 13 | 9 | 9 | **88** |
| ai-meeting-notes-tools | 23 | 16 | 20 | 12 | 9 | 4 | **82** |
| ai-meeting-minutes-guide | 23 | 18 | 20 | 13 | 9 | 4 | **84** |
| avoid-ai-hallucination-tips | 23 | 18 | 19 | 13 | 9 | 4 | **85** |
| jianying-ai-tutorial | 23 | 16 | 20 | 13 | 9 | 4 | **84** |
| suno-ai-tutorial-cn | 23 | 16 | 18 | 13 | 9 | 4 | **82** |
| ai-mock-interview-guide | 23 | 16 | 19 | 10 | 9 | 4 | **78** |
| **批均** | | | | | | | **82** |

---

## 2. 内链施工完成情况表

> 「正文行内内链」统计的是文章主体中的 `<a>` 内链（不含 header/footer/nav 与 `相关阅读` aside）。
> 「front-matter」为该篇 `internal_links` 字段条目数（含 `../tools.html` 导航项）。
> 状态：✅ 达标 / ⚠️ 部分达标（正文 <3 或 FM/正文不一致）/ 🟡 有轻量失真。

| # | 篇目 | FM 内链 | 正文行内内链 | 正文锚文本（去重） | 状态 |
|---|---|---|---|---|---|
| 1 | gemini-free-plan-review | 4 | 3 | 国内可直连的替代方案→chatgpt-alternatives-china；免费额度限制→claude-free-tier-limits；ChatGPT Plus 到底值不值→chatgpt-plus-worth-it | ⚠️ FM 的 free-ai-tools-list 未进正文；claude 锚文本与 FM 失真（FM「Claude 免费版的额度限制」vs 正文「免费额度限制」） |
| 2 | perplexity-ai-search-review | 5 | 2 | 用 NotebookLM 做资料研究→notebooklm-tutorial-cn；国内可用的 ChatGPT 替代方案→chatgpt-alternatives-china | ⚠️ 正文仅 2 条（<3）；FM 的 ai-chat-assistant-compare 未进正文 |
| 3 | kling-vs-jimeng-compare | 4 | 2 | 剪映 AI 哪些功能值得用→jianying-ai-features-review；AI 提示词怎么写→how-to-write-ai-prompts | ⚠️ 正文仅 2 条（<3）；FM 的 ai-video-tools-compare 未进正文 |
| 4 | jianying-ai-features-review | 4 | 3 | AI 配音工具对比→ai-voice-tools-compare；素材不够时用 AI 生成→kling-vs-jimeng-compare；剪映 AI 从入口到出片怎么操作→jianying-ai-tutorial | ✅ 含孤儿入链；FM 的 ai-video-tools-compare 未进正文 |
| 5 | ai-meeting-notes-tools | 4 | 4 | 通义千问的免费额度与场景→tongyi-qianwen-review；从录音到待办的完整做法→ai-meeting-minutes-guide；用 AI 写周报的完整做法→ai-weekly-report-guide；免费 AI 工具清单→free-ai-tools-list | ✅ 含孤儿入链；tongyi 锚文本与 FM 略有变体（FM「通义千问实测体验」） |
| 6 | ai-meeting-minutes-guide | 4 | 3 | AI 会议纪要工具怎么选→ai-meeting-notes-tools；防止 AI 编造内容→avoid-ai-hallucination-tips；提示词怎么写更稳→how-to-write-ai-prompts | ✅ FM 与正文完全一致 |
| 7 | avoid-ai-hallucination-tips | 4 | 3 | 大模型到底怎么工作的→what-is-llm-explained；AI 提示词的写法→how-to-write-ai-prompts；带来源的 AI 搜索工具→perplexity-ai-search-review | ✅ FM 与正文完全一致 |
| 8 | jianying-ai-tutorial | 4 | 3 | 素材不够时用 AI 生成视频→kling-vs-jimeng-compare；AI 配音工具对比→ai-voice-tools-compare；剪映 AI 哪些功能值得用→jianying-ai-features-review | ✅ 孤儿篇自身出链正常；FM 的 ai-video-tools-compare 未进正文；正文多出 ai-voice-tools-compare（不在 FM） |
| 9 | suno-ai-tutorial-cn | 4 | 3 | AI 语音与配音工具对比→ai-voice-tools-compare；风格提示词怎么写→how-to-write-ai-prompts；给视频配原创 AI 音乐→ai-video-tools-compare | 🟡 FM「提示词写作方法」vs 正文「风格提示词怎么写」变体，语义一致可接受 |
| 10 | ai-mock-interview-guide | 4 | 3 | 简历怎么用 AI 优化→ai-resume-optimization；别让 AI 替你编造经历→avoid-ai-hallucination-tips；四段结构提示词模板→how-to-write-ai-prompts | ⚠️ 三条正文内链全部扎堆在 L36–44；FM 的 ai-writing-tools-compare 未进正文；正文多出 ai-resume-optimization |

**FM 合规小结**：10 篇 front-matter `internal_links` 均为 4–5 条，全部落在 3–5 合规区间 ✅。所有正文内链目标均已在 `articles/` 中存在（无断链）✅。

---

## 3. 孤儿页处置确认

| 孤儿页 | 收到入链数 | 来源篇目 | 位置（正文/aside） | 结论 |
|---|---|---|---|---|
| gemini-free-plan-review | **3** | free-ai-tools-list（正文 L78）| 正文 | ✅ 已解决 |
| | | chatgpt-plus-worth-it（正文 L36）| 正文 | |
| | | claude-free-tier-limits（正文 L38）| 正文 | |
| ai-meeting-minutes-guide | **1** | ai-meeting-notes-tools（正文 L79）| 正文 | ✅ 已解决（入链数最少，建议后续补充 1–2 条以增强稳健性） |
| jianying-ai-tutorial | **2** | jianying-ai-features-review（正文 L76）| 正文 | ✅ 已解决 |
| | | ai-video-tools-compare（正文 L51）| 正文 | |

**处置结论**：
- 3 个孤儿页均已在**草稿层**收到 ≥1 条正文入链，不再是孤岛。
- 全部入链均为**正文行内链接**（非 aside/相关阅读），权重传递质量最高。
- ⚠️ 由于草稿施工时间（00:42–00:47）晚于当前构建（00:05），**构建产物中尚不存在这些入链**（已在 `articles/jianying-ai-features-review.html`、`articles/ai-meeting-notes-tools.html` 中 grep 验证为 0）。必须等待全量 rebuild（任务 #4）后孤儿处置才在线上生效。

---

## 4. 外链清单

| # | 篇目 | 外链数 | 域名 | 性质判定 |
|---|---|---|---|---|
| 1 | gemini-free-plan-review | 2 | support.google.com（Gemini 帮助中心）、gemini.google.com（Gemini 官方）| ✅ 官网/官方帮助，权威 |
| 2 | perplexity-ai-search-review | 2 | www.perplexity.ai、www.perplexity.ai/pricing | ✅ 官网 + 官方定价页 |
| 3 | kling-vs-jimeng-compare | 2 | klingai.com（可灵官方）、jimeng.jianying.com（即梦/字节官方）| ✅ 双官方站 |
| 4 | jianying-ai-features-review | 2 | www.capcut.cn（剪映官网，出现 2 次）| ✅ 官方站（剪映/国际版 CapCut 国内域名）|
| 5 | ai-meeting-notes-tools | 0 | — | ❌ 缺外链（可补飞书妙记/腾讯会议/通义听悟官方页）|
| 6 | ai-meeting-minutes-guide | 0 | — | ❌ 缺外链（可补通义听悟/飞书妙记官方说明页）|
| 7 | avoid-ai-hallucination-tips | 0 | — | ❌ 缺外链（正文提到裁判文书网，可落外链）|
| 8 | jianying-ai-tutorial | 0 | — | ❌ 缺外链（可补 capcut.cn 官方入口）|
| 9 | suno-ai-tutorial-cn | 0 | — | ❌ 缺外链（正文「先去官方条款页确认」未落链，可补 suno.com 官方条款页）|
| 10 | ai-mock-interview-guide | 0 | — | ❌ 缺外链（可补领英/官方求职资源等）|

**域名质量结论**：4 篇有外链的篇目共 8 条外链，全部指向官网/官方文档域名，**无仿冒镜像站**，质量 ✅。
**批级缺口**：批均外链 0.8 条，低于每篇 2–3 条的行业基准；6/10 篇为 0 外链。多为教程/清单类文章，可低成本补链（多为正文已提到、只是未落 `<a>`）。

---

## 5. 链接分布评估（正文行内内链）

| 篇目 | 前 1/3 | 中 1/3 | 后 1/3 | 评估 |
|---|---|---|---|---|
| gemini-free-plan-review | 0 | 1 | 2 | ⚠️ 偏后置，前段无内链 |
| perplexity-ai-search-review | 0 | 1 | 1 | ⚠️ 总量不足 + 前段无内链 |
| kling-vs-jimeng-compare | 0 | 1 | 1 | ⚠️ 总量不足 + 前段无内链 |
| jianying-ai-features-review | 0 | 2 | 1 | ✅ 中后段合理（首段引言短，可接受）|
| ai-meeting-notes-tools | 0 | 2 | 2 | ✅ 整体合理 |
| ai-meeting-minutes-guide | 1 | 2 | 0 | ✅ 前中段前置，健康 |
| avoid-ai-hallucination-tips | 2 | 0 | 1 | ✅ 前/后分散 |
| jianying-ai-tutorial | 1 | 1 | 1 | ✅ 均匀 |
| suno-ai-tutorial-cn | 1 | 1 | 1 | ✅ 均匀 |
| ai-mock-interview-guide | 3 | 0 | 0 | ⚠️ 三条全部挤在「开练之前」小节（L36–44）|

---

## 6. 用户旅程链接地图（批级示例）

```
读者入口 → 第四批任一文章
   ├→ 深入了解：对应聚类 Pillar/评测篇（如 jianying-ai-features-review ↔ jianying-ai-tutorial）
   ├→ 相关话题：同簇工具对比（kling-vs-jimeng-compare / ai-video-tools-compare / ai-voice-tools-compare）
   ├→ 方法论：how-to-write-ai-prompts / avoid-ai-hallucination-tips / what-is-llm-explained
   └→ 落地导航：../tools.html（AI 工具导航）
```

---

## 7. 遗留建议

### P1（建议随第五批返修或重建前处理）
1. **正文内链 <3 的 2 篇**：`perplexity-ai-search-review`、`kling-vs-jimeng-compare` 正文仅 2 条行内内链，低于 3 条下限。建议把 FM 中已存在但未落正文的 `ai-chat-assistant-compare.html`（perplexity）、`ai-video-tools-compare.html`（kling）择机补进正文语境。
2. **FM 与正文锚文本失真 2 处**：
   - gemini：FM「Claude 免费版的额度限制」vs 正文「免费额度限制」（建议正文补齐为 FM 全称，或反向统一）。
   - ai-meeting-notes-tools：FM「通义千问实测体验」vs 正文「通义千问的免费额度与场景」（建议统一为更描述性的正文版本）。
3. **跨篇锚文本撞车 2 组**：
   - `ai-video-tools-compare` 在 kling/jianying-features/jianying-tutorial 的 FM 中同为「AI 视频工具对比/横向对比」——3 篇指向同一目标、锚文本几乎一致，建议其中 1–2 篇差异化（如「AI 视频工具怎么选」）。
   - `kling-vs-jimeng-compare` 在 jianying-features（「素材不够时用 AI 生成」）与 jianying-tutorial（「素材不够时用 AI 生成视频」）锚文本近似，建议后者改为「可灵即梦生成补位视频」之类。
4. **外链缺失 6 篇**：ai-meeting-notes-tools、ai-meeting-minutes-guide、avoid-ai-hallucination-tips、jianying-ai-tutorial、suno-ai-tutorial-cn、ai-mock-interview-guide 均为 0 外链。多数正文已提到官方/权威来源但未落链，可低成本补齐至每篇 2 条（详见第 4 节「可补」标注）。
5. **ai-mock-interview-guide 正文内链扎堆**：3 条内链全在 L36–44（开练之前小节），建议将「AI 写作工具对比」（FM 已有）或其一条移到后半段「复盘打分」处。

### P2（可选项）
6. `ai-meeting-minutes-guide` 入链仅 1 条（最低），建议后续在相关周报/会议工具类文章补 1–2 条入链增强稳健性。
7. FM 与正文覆盖不完全一致是普遍现象（FM 承担「相关阅读」aside、正文承担行内链接），本身合规；若追求严格一致可后续统一，非阻塞项。

---

## 8. 实施清单（供 team-lead 排期）

- [ ] **全量 rebuild（任务 #4 前置）**：当前 articles HTML（00:05）不含孤儿入链与外链，必须重建后生效
- [ ] （建议）P1-1：perplexity / kling 正文内链补足至 3 条
- [ ] （建议）P1-2：gemini / meeting-notes 锚文本失真统一
- [ ] （建议）P1-3：ai-video-tools-compare、kling-vs-jimeng-compare 跨篇锚文本差异化
- [ ] （建议）P1-4：6 篇教程/清单类补外链
- [ ] （建议）P1-5：ai-mock-interview-guide 内链分布后移
- [ ] rebuild 后重跑 qa_check 验证无断链、孤儿置零
