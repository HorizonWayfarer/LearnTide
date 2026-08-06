# 第五批链接策略批级报告

- 批次：第五批（10 篇）
- 审计日期：2026-08-06
- 审计人：link-strategist（链接策略师）
- 审计性质：只读审计 + 健康度评分（不改草稿、不跑 build）
- 数据源：`drafts/*.md`（全站 60 篇草稿交叉核对）+ `qa_check.py`（当前 60 篇全通过）
- 状态说明：本批 10 篇**尚未进入 articles/**（构建产物中不存在），入链判断基于草稿层交叉引用与存量篇 FM 预埋

---

## 0. 关键结论（TL;DR）

1. **批均内容健康度：84 / 100**，10 篇得分 76–90，无不及格。
2. **FM internal_links 全部 3–5 合规 ✅**；正文行内内链 10/10 ≥3；无断链（qa_check 0 FAIL）。
3. **外链 10/10 篇均有 2 条，全部官网/官方域名，无仿冒镜像 ✅**。其中 suno 链接为 suno.com / suno.com/pricing（官方），未踩 suno-v5/zh 类镜像。
4. **⚠️ 孤岛偏多：10 篇里有 7 篇收不到任何入链**（wenxin-yiyan-review、midjourney-worth-subscribing、miota-writing-cat-review、best-ai-apps-mobile、ai-paper-rewrite-tips、jimeng-prompt-tips、jobs-replaced-by-ai）。仅 cursor-beginner-tutorial（3 条）、ai-excel-tutorial（1 条）、suno-ai-music-review（1 条 aside）有人链。
5. **遗留重点**：P1-1 孤岛处置（7 篇需补正文入链）；P1-2 ai-paper-rewrite-tips 同目标重复内链（how-to-write-ai-prompts 正文出现 2 次）；P1-3 ai-excel-tutorial FM/正文覆盖不一致（ai-meeting-notes-tools 在 FM 未进正文）；P2 剪映官网域名跨批不一致（batch4 用 capcut.cn，本篇用 lv.ulikecam.com）。

---

## 1. 批均内容健康度评分

### 1.1 评分框架（沿用批级口径）

| 维度 | 权重 | 说明 |
|---|---|---|
| 链接完整性 | 25% | FM 3–5、正文 ≥3、无断链、FM/正文一致 |
| 锚文本质量 | 20% | 描述性、跨篇不撞车、正文内不重复 |
| 聚类连通性 | 20% | 收到入链（正文 > aside > 0）、与聚类互链 |
| 链接分布 | 15% | 前/中/后三段分布 |
| 用户价值 | 10% | 每条链接对读者有用 |
| 竞品对标 | 10% | 外链数量与官方域名质量 |

### 1.2 各篇得分

| 篇目 | 链接完整性 | 锚文本 | 聚类连通 | 分布 | 用户价值 | 竞品对标 | 总分 |
|---|---|---|---|---|---|---|---|
| wenxin-yiyan-review | 24 | 18 | 10 | 14 | 9 | 9 | **84** |
| midjourney-worth-subscribing | 24 | 18 | 10 | 14 | 9 | 9 | **84** |
| suno-ai-music-review | 24 | 18 | 14 | 14 | 9 | 9 | **88** |
| miota-writing-cat-review | 24 | 18 | 10 | 14 | 9 | 9 | **84** |
| best-ai-apps-mobile | 24 | 17 | 10 | 11 | 9 | 8 | **79** |
| ai-paper-rewrite-tips | 22 | 15 | 10 | 14 | 9 | 9 | **79** |
| ai-excel-tutorial | 22 | 18 | 16 | 13 | 9 | 9 | **87** |
| jimeng-prompt-tips | 24 | 18 | 10 | 14 | 9 | 9 | **84** |
| cursor-beginner-tutorial | 25 | 18 | 18 | 14 | 9 | 9 | **93** |
| jobs-replaced-by-ai | 24 | 18 | 10 | 14 | 9 | 10 | **85** |
| **批均** | | | | | | | **84** |

---

## 2. 内链施工完成情况表

> 正文行内内链 = 文章主体 `<a>` 内链（不含 aside）；FM 为该篇 `internal_links` 条目数。
> 状态：✅ 达标 / ⚠️ 部分达标（FM/正文不一致或正文重复）/ 🟡 有轻量问题。

| # | 篇目 | FM | 正文内链 | 正文锚文本（去重） | 状态 |
|---|---|---|---|---|---|
| 1 | wenxin-yiyan-review | 4 | 4 | 通义千问测评→tongyi-qianwen-review；国内 ChatGPT 替代品→chatgpt-alternatives-china；国内大模型全景→china-llm-landscape-2026；提示词写法→how-to-write-ai-prompts | ✅ FM 与正文完全一致 |
| 2 | midjourney-worth-subscribing | 3 | 3 | 提示词技巧→midjourney-prompt-tips；即梦 AI 测评→jimeng-ai-review；免费替代工具→midjourney-free-alternatives | ✅ FM 与正文完全一致 |
| 3 | suno-ai-music-review | 3 | 3 | Suno 中文教程→suno-ai-tutorial-cn；AI 语音工具对比→ai-voice-tools-compare；AI 视频工具对比→ai-video-tools-compare | ✅ FM 与正文完全一致 |
| 4 | miota-writing-cat-review | 3 | 3 | AI 写作工具对比→ai-writing-tools-compare；去除 AI 腔调→remove-ai-tone-writing；AI 论文写作指南→ai-thesis-writing-guide | ✅ FM 与正文完全一致 |
| 5 | best-ai-apps-mobile | 4 | 4 | 豆包 vs Kimi 对比→doubao-vs-kimi-compare；通义千问测评→tongyi-qianwen-review；即梦 AI 测评→jimeng-ai-review；免费 AI 工具清单→free-ai-tools-list | ✅ FM 与正文完全一致 |
| 6 | ai-paper-rewrite-tips | 4 | 4 | 去掉 AI 味的具体改法→remove-ai-tone-writing；怎么写提示词→how-to-write-ai-prompts；提示词写法→how-to-write-ai-prompts；AI 辅助论文写作的完整流程→ai-thesis-writing-guide | ⚠️ how-to-write-ai-prompts 在正文出现 **2 次**（L42+L59），且 L42 锚文本与 FM「提示词写法」不一致 |
| 7 | ai-excel-tutorial | 5 | 3 | 把需求说清楚的提示词方法→how-to-write-ai-prompts；免费可用的 AI 工具→free-ai-tools-list；怎么防 AI 一本正经胡说→avoid-ai-hallucination-tips | ⚠️ FM 的 ai-meeting-notes-tools 未进正文 |
| 8 | jimeng-prompt-tips | 4 | 4 | 提示词写法→how-to-write-ai-prompts；Midjourney 提示词技巧→midjourney-prompt-tips；可灵和即梦怎么选→kling-vs-jimeng-compare；即梦 AI 的实际表现→jimeng-ai-review | ✅ FM 与正文完全一致 |
| 9 | cursor-beginner-tutorial | 5 | 5 | AI 工具导航→../tools.html；Cursor 和 Copilot 哪个好→cursor-vs-copilot-compare；AI 提示词怎么写→how-to-write-ai-prompts；AI 编程助手哪个好→ai-coding-assistants-compare；什么是 AI Agent→what-is-ai-agent | ✅ FM 与正文完全一致（含 tools.html） |
| 10 | jobs-replaced-by-ai | 5 | 5 | 2026 年 AI 趋势→ai-trends-2026；AI 工具导航→../tools.html；什么是 AI Agent→what-is-ai-agent；AI 模拟面试→ai-mock-interview-guide；用 AI 优化简历→ai-resume-optimization | ✅ FM 与正文完全一致（含 tools.html） |

**小结**：10/10 篇 FM 3–5 合规；正文内链 10/10 ≥3；所有正文内链目标均已上线（qa_check 0 FAIL）。2 处 FM/正文不一致（ai-excel-tutorial、ai-paper-rewrite-tips 重复）。

---

## 3. 孤岛检查（本批入链情况）

> 入链来源标注「正文 / FM-aside」；FM-aside 即存量篇 `相关阅读` 模块渲染的预埋入链（构建后生效）。

| 篇目 | 入链数 | 来源 | 结论 |
|---|---|---|---|
| wenxin-yiyan-review | 0 | — | ⚠️ **孤岛** |
| midjourney-worth-subscribing | 0 | — | ⚠️ **孤岛** |
| suno-ai-music-review | 1 | ai-voice-tools-compare（FM-aside） | 🟡 弱入链（仅 aside） |
| miota-writing-cat-review | 0 | — | ⚠️ **孤岛** |
| best-ai-apps-mobile | 0 | — | ⚠️ **孤岛** |
| ai-paper-rewrite-tips | 0 | — | ⚠️ **孤岛** |
| ai-excel-tutorial | 1 | notion-ai-worth-it（FM-aside + 正文） | ✅ 已解决 |
| jimeng-prompt-tips | 0 | — | ⚠️ **孤岛** |
| cursor-beginner-tutorial | 3 | ai-build-webpage-nocode（FM+正文）；ai-coding-assistants-compare（FM）；tongyi-lingma-review（FM+正文） | ✅ 健康 |
| jobs-replaced-by-ai | 0 | — | ⚠️ **孤岛** |

**孤岛结论**：本批 **7 篇孤岛**（0 入链）。原因判断：第五批为新写批次，存量篇 FM 预埋只覆盖了 cursor 系与部分工具对比类，中文写作/剪辑/清单类未做预埋，且本批内部互链稀疏。建议在后续批次或返修轮统一补齐正文入链（详见遗留建议 P1-1）。

---

## 4. 外链清单（域名质量）

| # | 篇目 | 外链数 | 域名 | 判定 |
|---|---|---|---|---|
| 1 | wenxin-yiyan-review | 2 | yige.baidu.com（文心一格）、yiyan.baidu.com（文心一言）| ✅ 百度官方 |
| 2 | midjourney-worth-subscribing | 2 | docs.midjourney.com/docs/plans、www.midjourney.com | ✅ 官方文档+官网 |
| 3 | suno-ai-music-review | 2 | suno.com/pricing、suno.com | ✅ 官网+官方定价（未踩 suno-v5/zh 镜像）|
| 4 | miota-writing-cat-review | 2 | xiezuocat.com/help、xiezuocat.com | ✅ 秘塔官方 |
| 5 | best-ai-apps-mobile | 2 | lv.ulikecam.com（剪映专业版官网）、jimeng.jianying.com（即梦官网）| ✅ 均官方（字节系）；🟡 剪映域名与 batch4 的 capcut.cn 不一致，见 P2 |
| 6 | ai-paper-rewrite-tips | 2 | cx.cnki.net（知网个人查重）、moe.gov.cn（教育部学位法全文）| ✅ 官方/政务权威 |
| 7 | ai-excel-tutorial | 2 | support.microsoft.com/zh-cn/copilot-excel、ai.wps.cn | ✅ 微软官方+WPS AI 官方 |
| 8 | jimeng-prompt-tips | 2 | jimeng.jianying.com、docs.midjourney.com | ✅ 官方 |
| 9 | cursor-beginner-tutorial | 2 | cursor.com、cursor.com/help | ✅ 官网+帮助页 |
| 10 | jobs-replaced-by-ai | 2 | paper.people.com.cn（人民日报·中国经济周刊）、weforum.org（世界经济论坛）| ✅ 权威官方 |

**域名质量结论**：10/10 篇有外链（各 2 条），共 20 条全部为官网/官方文档/政务权威域名，**无仿冒镜像**。suno 相关正确指向 suno.com，未出现 suno-zh / suno-v5/v6 类镜像；无 runwaychina.com 类仿冒。

---

## 5. 链接分布评估（正文行内内链，近似）

| 篇目 | 前 1/3 | 中 1/3 | 后 1/3 | 评估 |
|---|---|---|---|---|
| wenxin-yiyan-review | 2 | 1 | 1 | ✅ |
| midjourney-worth-subscribing | 0 | 2 | 1 | 🟡 前段无内链（可接受）|
| suno-ai-music-review | 0 | 2 | 1 | 🟡 前段无内链 |
| miota-writing-cat-review | 0 | 2 | 1 | 🟡 前段无内链 |
| best-ai-apps-mobile | 1 | 2 | 1 | ✅ |
| ai-paper-rewrite-tips | 0 | 3 | 1 | 🟡 中段偏密（含重复链接）|
| ai-excel-tutorial | 0 | 1 | 2 | ✅ 后置可接受 |
| jimeng-prompt-tips | 1 | 2 | 1 | ✅ |
| cursor-beginner-tutorial | 1 | 2 | 2 | ✅ |
| jobs-replaced-by-ai | 1 | 2 | 2 | ✅ |

---

## 6. 遗留建议

### P1（建议返修轮处理）
1. **孤岛 7 篇补正文入链**：wenxin-yiyan-review、midjourney-worth-subscribing、miota-writing-cat-review、best-ai-apps-mobile、ai-paper-rewrite-tips、jimeng-prompt-tips、jobs-replaced-by-ai 均 0 入链。建议：
   - wenxin ← china-llm-landscape-2026 / chatgpt-alternatives-china 正文补链（同类横评）；
   - midjourney-worth ← midjourney-prompt-tips / jimeng-ai-review 正文补链；
   - miota-writing-cat ← ai-writing-tools-compare / ai-thesis-writing-guide 正文补链；
   - best-ai-apps-mobile ← free-ai-tools-list / doubao-vs-kimi-compare 正文补链；
   - ai-paper-rewrite ← ai-thesis-writing-guide / remove-ai-tone-writing 正文补链；
   - jimeng-prompt-tips ← jimeng-ai-review / kling-vs-jimeng-compare 正文补链；
   - jobs-replaced-by-ai ← ai-trends-2026 / what-is-ai-agent 正文补链。
2. **ai-paper-rewrite-tips 同目标重复内链**：how-to-write-ai-prompts 在正文出现 2 次（L42「怎么写提示词」+ L59「提示词写法」），建议删除或替换其一（例如 L42 改为链向 ai-prompt-formula-template 或改述）。
3. **ai-excel-tutorial FM/正文覆盖不一致**：FM 的 ai-meeting-notes-tools「AI 整理会议纪要工具」未进正文，可在「哪些表不能传/路线选择」语境补一句正文链接，或从 FM 移除保持一致。

### P2（可选项）
4. **剪映官网域名跨批统一**：batch4 用 www.capcut.cn，本篇 best-ai-apps-mobile 用 lv.ulikecam.com（均为字节官方，但口径不一；另有 jianying.com 新站）。建议全站统一为同一官方域名。
5. **suno-ai-music-review 弱入链增强**：目前仅 ai-voice-tools-compare 的 aside 预埋，建议 suno-ai-tutorial-cn 或 ai-video-tools-compare 正文补一条入链。
6. **best-ai-apps-mobile 可读性**：qa 显示短句 3% / 均句长 32.0（WARN，非链接问题，属内容侧，任务 #16 已在跟进）。

---

## 7. 实施清单（供 team-lead 排期）

- [ ] P1-1：7 篇孤岛补正文入链（详见第 6 节）
- [ ] P1-2：ai-paper-rewrite-tips 消除 how-to-write-ai-prompts 正文重复
- [ ] P1-3：ai-excel-tutorial FM/正文对齐
- [ ] P2：剪映域名统一、suno-ai-music-review 补正文入链
- [ ] 本批尚在 drafts，未构建；上述施工完成后随全量 rebuild 上线
