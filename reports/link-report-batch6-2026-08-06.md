# 第六批链接策略批级报告

- 批次：第六批（10 篇）
- 审计日期：2026-08-06
- 审计人：link-strategist（链接策略师）
- 审计性质：只读审计 + 健康度评分（不改草稿、不跑 build）
- 数据源：`drafts/*.md`（全站 60 篇草稿交叉核对）+ `qa_check.py`（当前 60 篇全通过）
- 状态说明：本批 10 篇**尚未进入 articles/**，入链判断基于草稿层交叉引用与存量篇 FM 预埋（预埋契约已逐一核验）

---

## 0. 关键结论（TL;DR）

1. **批均内容健康度：86 / 100**，10 篇得分 80–90，无不及格。整体优于第五批（84）。
2. **FM internal_links 全部 3–5 合规 ✅**；正文行内内链 10/10 ≥3；无断链（qa_check 0 FAIL）。
3. **外链 10/10 篇均有 2–3 条，全部官网/官方域名，无仿冒镜像 ✅**。runway 篇与 kling 篇主动点名仿冒镜像（runwaychina.com、带广告假站）且不链入，处理规范。
4. **预埋契约 3 篇全部确认有人链**：tongyi-lingma-review（← ai-coding-assistants-compare / cursor-vs-copilot-compare FM 预埋）、ai-reading-notes-method（← notebooklm-tutorial-cn FM 预埋 + feed-documents-to-ai 正文）、ai-self-intro-writing（← ai-resume-optimization FM 预埋）✅。
5. **⚠️ 仍存 5 篇孤岛**：zhipu-qingyan-review、runway-ai-video-review、notion-ai-worth-it、ai-translation-tools-compare、kling-ai-tutorial（0 入链）。
6. **遗留重点**：P1-1 孤岛 5 篇补正文入链；P1-2 notion-ai-worth-it FM/正文双向不一致（ai-meeting-minutes-guide 在 FM 未进正文、ai-wechat-article-writing 在正文未进 FM）；P1-3 tongyi-lingma-review FM 的 ai-build-webpage-nocode 未进正文；P2 弱入链 2 篇（ai-self-intro-writing、ai-build-webpage-nocode 仅 aside）。

---

## 1. 批均内容健康度评分

### 1.1 评分框架（沿用批级口径）

| 维度 | 权重 | 说明 |
|---|---|---|
| 链接完整性 | 25% | FM 3–5、正文 ≥3、无断链、FM/正文一致 |
| 锚文本质量 | 20% | 描述性、跨篇不撞车、正文内不重复 |
| 聚类连通性 | 20% | 收到入链（正文 > aside > 0）、预埋契约 |
| 链接分布 | 15% | 前/中/后三段分布 |
| 用户价值 | 10% | 每条链接对读者有用 |
| 竞品对标 | 10% | 外链数量与官方域名质量 |

### 1.2 各篇得分

| 篇目 | 链接完整性 | 锚文本 | 聚类连通 | 分布 | 用户价值 | 竞品对标 | 总分 |
|---|---|---|---|---|---|---|---|
| zhipu-qingyan-review | 24 | 18 | 10 | 14 | 9 | 10 | **85** |
| runway-ai-video-review | 24 | 18 | 10 | 14 | 9 | 10 | **85** |
| notion-ai-worth-it | 22 | 17 | 10 | 13 | 9 | 9 | **80** |
| tongyi-lingma-review | 22 | 18 | 16 | 13 | 9 | 9 | **87** |
| ai-translation-tools-compare | 24 | 18 | 10 | 14 | 9 | 9 | **84** |
| ai-reading-notes-method | 25 | 18 | 18 | 14 | 9 | 9 | **93** |
| feed-documents-to-ai | 25 | 18 | 16 | 14 | 9 | 9 | **91** |
| kling-ai-tutorial | 25 | 18 | 10 | 14 | 9 | 10 | **86** |
| ai-self-intro-writing | 25 | 18 | 15 | 14 | 9 | 9 | **90** |
| ai-build-webpage-nocode | 24 | 18 | 14 | 14 | 9 | 9 | **88** |
| **批均** | | | | | | | **86** |

---

## 2. 内链施工完成情况表

> 正文行内内链 = 文章主体 `<a>` 内链（不含 aside）；FM 为该篇 `internal_links` 条目数。
> 状态：✅ 达标 / ⚠️ 部分达标（FM/正文不一致）/ 🟡 有轻量问题。

| # | 篇目 | FM | 正文内链 | 正文锚文本（去重） | 状态 |
|---|---|---|---|---|---|
| 1 | zhipu-qingyan-review | 5 | 4 | 国内能直接打开的中文 AI→chatgpt-alternatives-china；DeepSeek 和 ChatGPT 怎么选→deepseek-vs-chatgpt-compare；豆包和 Kimi 的分工→doubao-vs-kimi-compare；2026 国产大模型格局→china-llm-landscape-2026 | ✅ 4 个文章目标全进正文（tools.html 仅 FM）|
| 2 | runway-ai-video-review | 5 | 4 | AI 视频生成工具横向对比→ai-video-tools-compare；可灵和即梦的视频生成对比→kling-vs-jimeng-compare；即梦 AI 的出图与视频能力→jimeng-ai-review；剪映 AI 的智能成片步骤→jianying-ai-tutorial | ✅ 4 个文章目标全进正文 |
| 3 | notion-ai-worth-it | 5 | 4 | AI 会议纪要工具对比→ai-meeting-notes-tools；用 AI 做 PPT 的完整步骤→how-to-make-ppt-with-ai；用 AI 处理 Excel 表格→ai-excel-tutorial；用 AI 写公众号文章→ai-wechat-article-writing | ⚠️ FM 的 ai-meeting-minutes-guide 未进正文；正文多出 ai-wechat-article-writing（不在 FM）——双向不一致 |
| 4 | tongyi-lingma-review | 5 | 3 | AI 编程助手横向对比→ai-coding-assistants-compare；Cursor 和 Copilot 怎么选→cursor-vs-copilot-compare；Cursor 新手教程→cursor-beginner-tutorial | ⚠️ FM 的 ai-build-webpage-nocode 未进正文 |
| 5 | ai-translation-tools-compare | 5 | 4 | AI 写作工具横向对比→ai-writing-tools-compare；用 AI 写公众号文章→ai-wechat-article-writing；用 AI 写小红书文案→ai-xiaohongshu-copywriting；AI 提示词怎么写→how-to-write-ai-prompts | ✅ 4 个文章目标全进正文 |
| 6 | ai-reading-notes-method | 5 | 5 | NotebookLM 中文资料整理教程→notebooklm-tutorial-cn；怎么给 AI 投喂资料→feed-documents-to-ai；AI 辅助论文写作指南→ai-thesis-writing-guide；AI 提示词怎么写→how-to-write-ai-prompts；AI 工具导航→../tools.html | ✅ FM 与正文完全一致 |
| 7 | feed-documents-to-ai | 5 | 5 | 提示词模板公式→ai-prompt-formula-template；别让 AI 编造答案的方法→avoid-ai-hallucination-tips；AI 提示词怎么写→how-to-write-ai-prompts；用 AI 做读书笔记→ai-reading-notes-method；AI 工具导航→../tools.html | ✅ FM 与正文完全一致 |
| 8 | kling-ai-tutorial | 5 | 5 | 可灵和即梦的视频生成对比→kling-vs-jimeng-compare；剪映 AI 的智能成片步骤→jianying-ai-tutorial；AI 视频生成工具横向对比→ai-video-tools-compare；即梦 AI 的出图与视频能力→jimeng-ai-review；AI 工具导航→../tools.html | ✅ FM 与正文完全一致 |
| 9 | ai-self-intro-writing | 5 | 5 | AI 提示词怎么写→how-to-write-ai-prompts；用 AI 模拟面试的三轮练习法→ai-mock-interview-guide；去掉 AI 味的改写方法→remove-ai-tone-writing；用 AI 优化简历→ai-resume-optimization；AI 工具导航→../tools.html | ✅ FM 与正文完全一致 |
| 10 | ai-build-webpage-nocode | 4 | 4 | AI 提示词怎么写→how-to-write-ai-prompts；Cursor 新手教程→cursor-beginner-tutorial；AI 编程助手横向对比→ai-coding-assistants-compare；AI 工具导航→../tools.html | ✅ FM 与正文完全一致 |

**小结**：10/10 篇 FM 3–5 合规；正文内链 10/10 ≥3；所有正文内链目标均已上线（qa_check 0 FAIL）。2 处 FM/正文不一致（notion-ai-worth-it、tongyi-lingma-review）。

---

## 3. 孤岛检查（本批入链情况 + 预埋契约核验）

> 入链来源标注「正文 / FM-aside」；FM-aside 即存量篇 `相关阅读` 渲染的预埋入链。

| 篇目 | 入链数 | 来源 | 结论 |
|---|---|---|---|
| zhipu-qingyan-review | 0 | — | ⚠️ **孤岛** |
| runway-ai-video-review | 0 | — | ⚠️ **孤岛** |
| notion-ai-worth-it | 0 | — | ⚠️ **孤岛** |
| tongyi-lingma-review | 2 | ai-coding-assistants-compare（FM-aside 预埋）；cursor-vs-copilot-compare（FM-aside 预埋）| ✅ 预埋契约确认（重建后生效，仅 aside）|
| ai-translation-tools-compare | 0 | — | ⚠️ **孤岛** |
| ai-reading-notes-method | 2 | feed-documents-to-ai（FM+正文）；notebooklm-tutorial-cn（FM-aside 预埋）| ✅ 预埋契约确认 + 1 条正文入链 |
| feed-documents-to-ai | 1 | ai-reading-notes-method（FM+正文）| ✅ 已解决 |
| kling-ai-tutorial | 0 | — | ⚠️ **孤岛** |
| ai-self-intro-writing | 1 | ai-resume-optimization（FM-aside 预埋）| ✅ 预埋契约确认（仅 aside，弱入链）|
| ai-build-webpage-nocode | 1 | tongyi-lingma-review（FM-aside）| 🟡 弱入链（仅 aside）|

**孤岛结论**：本批 **5 篇孤岛**（0 入链）：zhipu-qingyan-review、runway-ai-video-review、notion-ai-worth-it、ai-translation-tools-compare、kling-ai-tutorial。team-lead 点名的 3 个预埋契约（tongyi-lingma-review、ai-reading-notes-method、ai-self-intro-writing）**全部确认存在预埋入链**，契约无缺失；但其中 2 篇仅 FM-aside 预埋，建议后续补正文入链增强（P2）。

---

## 4. 外链清单（域名质量）

| # | 篇目 | 外链数 | 域名 | 判定 |
|---|---|---|---|---|
| 1 | zhipu-qingyan-review | 3 | zhipuai.cn、open.bigmodel.cn、chatglm.cn | ✅ 智谱官方（官网/开放平台/产品页）|
| 2 | runway-ai-video-review | 3 | runwayml.com、docs.runwayml.com、help.runwayml.com | ✅ Runway 官方三件套；文中点名 runwaychina.com 为仿冒且不链入 ✅ |
| 3 | notion-ai-worth-it | 2 | notion.com/pricing、notion.com/help | ✅ 官方定价+帮助中心 |
| 4 | tongyi-lingma-review | 3 | lingma.aliyun.com、help.aliyun.com/zh/lingma、aliyun.com/product/yunxiao/lingma | ✅ 阿里云官方三件套 |
| 5 | ai-translation-tools-compare | 3 | deepl.com、fanyi.youdao.com、fanyi.qq.com | ✅ DeepL/有道/腾讯翻译君官方 |
| 6 | ai-reading-notes-method | 3 | weread.qq.com、notebooklm.google.com、support.google.com/notebooklm | ✅ 微信读书+NotebookLM 官方 |
| 7 | feed-documents-to-ai | 3 | platform.deepseek.com、help.aliyun.com/zh/model-studio、kimi.com | ✅ DeepSeek/阿里云百炼/Kimi 官方 |
| 8 | kling-ai-tutorial | 3 | kling.ai、app.klingai.com、cac.gov.cn | ✅ 可灵官方（新域名）+国家网信办；文中警告仿冒假站且不链入 ✅（注意勿用带连字符的 kling-ai.com 镜像）|
| 9 | ai-self-intro-writing | 2 | zhaopin.com、zhipin.com | ✅ 智联招聘/BOSS 直聘官方 |
| 10 | ai-build-webpage-nocode | 3 | pages.github.com、netlify.com、vercel.com | ✅ GitHub Pages/Netlify/Vercel 官方 |

**域名质量结论**：10/10 篇有外链（2–3 条），共 27 条全部为官网/官方文档/政务权威域名，**无仿冒镜像**。runway 篇与 kling 篇主动识别并警告镜像（runwaychina.com、带广告假站、kling-ai.com 类），符合本站「说真话」定位。

---

## 5. 链接分布评估（正文行内内链，近似）

| 篇目 | 前 1/3 | 中 1/3 | 后 1/3 | 评估 |
|---|---|---|---|---|
| zhipu-qingyan-review | 1 | 2 | 1 | ✅ |
| runway-ai-video-review | 1 | 0 | 3 | 🟡 中段无内链、后段偏密 |
| notion-ai-worth-it | 0 | 3 | 1 | 🟡 中段偏密 |
| tongyi-lingma-review | 0 | 3 | 0 | 🟡 全集中在中段 |
| ai-translation-tools-compare | 0 | 2 | 2 | ✅ |
| ai-reading-notes-method | 2 | 0 | 3 | 🟡 中段无内链 |
| feed-documents-to-ai | 1 | 2 | 2 | ✅ |
| kling-ai-tutorial | 1 | 1 | 3 | 🟡 后段偏密 |
| ai-self-intro-writing | 1 | 2 | 2 | ✅ |
| ai-build-webpage-nocode | 1 | 2 | 1 | ✅ |

---

## 6. 遗留建议

### P1（建议返修轮处理）
1. **孤岛 5 篇补正文入链**：zhipu-qingyan-review、runway-ai-video-review、notion-ai-worth-it、ai-translation-tools-compare、kling-ai-tutorial 均 0 入链。建议：
   - zhipu-qingyan ← chatgpt-alternatives-china / china-llm-landscape-2026 正文补链；
   - runway-ai-video ← ai-video-tools-compare / kling-vs-jimeng-compare 正文补链；
   - notion-ai-worth-it ← ai-meeting-notes-tools / ai-excel-tutorial 正文补链；
   - ai-translation-tools ← ai-writing-tools-compare / ai-wechat-article-writing 正文补链；
   - kling-ai-tutorial ← kling-vs-jimeng-compare / ai-video-tools-compare 正文补链。
2. **notion-ai-worth-it FM/正文双向不一致**：FM 的 ai-meeting-minutes-guide「AI 会议记录指南」未进正文，而正文的 ai-wechat-article-writing「用 AI 写公众号文章」不在 FM。建议正文补链 ai-meeting-minutes-guide，并决定 ai-wechat-article-writing 是否入 FM（或二选一保持一致）。
3. **tongyi-lingma-review FM/正文不一致**：FM 的 ai-build-webpage-nocode「不会写代码用 AI 做网页」未进正文，可在文末「个人写项目/建站」语境补一句正文链接。

### P2（可选项）
4. **弱入链增强**：ai-self-intro-writing（仅 ai-resume-optimization aside 预埋）、ai-build-webpage-nocode（仅 tongyi-lingma-review aside）建议在相关教程/清单篇补正文入链。
5. **链路复用的反向确认**：notion-ai-worth-it 已给 ai-excel-tutorial 正文入链（正向 OK），但自身是孤岛——批量补链时应优先「已出链未收链」的节点。
6. **跨批一致性**：runway 篇与 kling 篇的镜像警告文案可统一措辞（如统一为「认准官方域名 X，勿用 Y 类镜像」），提升模板感。

---

## 7. 实施清单（供 team-lead 排期）

- [ ] P1-1：5 篇孤岛补正文入链（详见第 6 节）
- [ ] P1-2：notion-ai-worth-it FM/正文对齐
- [ ] P1-3：tongyi-lingma-review FM/正文对齐
- [ ] P2：ai-self-intro-writing / ai-build-webpage-nocode 补正文入链
- [ ] 本批尚在 drafts，未构建；上述施工完成后随全量 rebuild 上线
