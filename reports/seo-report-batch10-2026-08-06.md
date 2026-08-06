# LearnTide 第十批 SEO 技术审计报告

> 审计日期：2026-08-06
> 审计人：seo-optimizer-3（欧化成）
> 审计范围：第十批 10 篇文章（已通过 qa_check 0 FAIL，已构建上线，全站 103 篇）
> 报告路径：`A:\LearnTide\reports\seo-report-batch10-2026-08-06.md`
> 对标标准：延续第 8/9 批口径——密度以中文字数为分母、规范化命中（忽略大小写/空格）为准；Meta 宽度为显示宽度（CJK×2），题宽 52–64 / 述宽 145–162；外链仅认官方/权威域名，仿冒镜像不得链入。

---

## 一、批级 SEO 评分

### 综合评分：84 / 100 — ❌ 不合格（存在 1 项 P0 红线）

> 判定：第 10 批 **发现 1 个 P0**（free-ai-code-completion-tools 残留旧品牌名「通义灵码」）。按批次红线规则「无 P0 且综合 ≥70 才算合格」，**本批判定为不合格**，需修复 P0 后复评。其余 9 篇均为「可发布」质量。

| 维度 | 得分 | 满分 | 说明 |
|------|------|------|------|
| 关键词优化 | 16 | 25 | 前 100 字覆盖 10/10 ✅；H2 含主词 10/10 满足最低 1（理想 2 仅 0 篇）；密度规范化 4/10 达 ≥1.0%，4 篇 0.90–0.99% 临界，2 篇 <0.90%（free-ai-code 0.82、privacy 0.89） |
| 内容质量与精选摘要 | 22 | 25 | 全批结论前置 + 直答 + 关键要点/表格/提示词块，精选摘要机会 10/10 优良 |
| Meta 元素 | 25 | 25 | 题宽 10/10（54–62）、述宽 10/10（146–159）全部合格；主词均入 Meta |
| 结构与链接 | 19 | 25 | 内链 10/10 无断链；外链全为官方意图但 **2 篇含失效/错误域名**（qoder.aliyun.com 域名不存在、gov.cn 个保法链接跳首页）；外链数 2 篇仅 1 条 |
| 诚信合规 | 15 | 25 | **P0×1**（旧品牌名残留）；禁词实测/待核实/TODO 全批 0；仿冒镜像未链入 ✅；法律话题软表述与法条数字准确 ✅ |

---

## 二、逐篇评分表

| # | 文章 | ID | 密度(规范化) | 前100 | H2含主词 | 题宽 | 述宽 | 外链(官方) | 内链 | P0 | 综合 |
|---|------|-----|-------------|-------|---------|------|------|-----------|------|-----|------|
| 1 | grammarly-free-alternatives | 028 | 1.06% ✅ | ✓ | 1/5 | 56 ✅ | 146 ✅ | 2（grammarly.com、languagetool.org）✅ | 5 | 无 | 90 |
| 2 | free-ai-code-completion-tools | 033 | 0.82% ✗ | ✓ | 1/5 | 54 ✅ | 154 ✅ | 2（**qoder.aliyun.com 失效**⚠️、codeium.com）| 7 | **P0** | 55 |
| 3 | ai-id-photo-tutorial | 060 | 0.92% ⚠️ | ✓ | 1/5 | 62 ✅ | 151 ✅ | 2（meitu.com、gov.cn）✅ | 6 | 无 | 86 |
| 4 | ai-avatar-generation-guide | 062 | 0.99% ⚠️ | ✓ | 1/5 | 56 ✅ | 159 ✅ | 2（jimeng.jianying.com、doubao.com）✅ | 10 | 无 | 87 |
| 5 | ai-audiobook-guide | 069 | 1.00% ✅ | ✓ | 1/5 | 54 ✅ | 150 ✅ | 2（xfyun.cn、cloud.baidu.com）✅ | 8 | 无 | 90 |
| 6 | ai-travel-planning-guide | 075 | 1.34% ✅ | ✓ | 1/5 | 56 ✅ | 157 ✅ | 1（12306.cn）✅ | 6 | 无 | 88 |
| 7 | what-is-token-ai | 082 | 0.90% ⚠️ | ✓ | 1/5 | 60 ✅ | 150 ✅ | 2（platform.openai.com、help.openai.com）✅ | 8 | 无 | 86 |
| 8 | what-is-prompt-engineering | 084 | 1.01% ✅ | ✓ | 1/5 | 54 ✅ | 150 ✅ | 2（help.openai.com、docs.anthropic.com）✅ | 6 | 无 | 90 |
| 9 | ai-content-copyright-cn | 095 | 0.92% ⚠️ | ✓ | 1/5 | 59 ✅ | 157 ✅ | 1（gov.cn 标识办法，有效）✅ | 4 | 无 | 87 |
| 10 | ai-privacy-data-safety | 097 | 0.89% ✗ | ✓ | 1/5 | 56 ✅ | 150 ✅ | 2（cac.gov.cn ✅、**gov.cn 个保法失效**⚠️）| 4 | 无 | 84 |

> 密度为规范化命中（大小写/空格归一），如「AI 做旅行攻略」计入「ai做旅行攻略」主词。目标 1–2%（≈正文中文字数×1%～×2%）。✅≥1.00%，⚠️0.90–0.99%，✗<0.90%。
> 外链括号内为实测域名；⚠️ 表示失效/错误域名（详见 P1）。
> 内链数为渲染页面实际内链数（含相关阅读），全批无断链。

---

## 三、P0 / P1 / P2 问题清单

### P0 — 诚信红线（必须修复，本批 1 项）

#### P0-1：free-ai-code-completion-tools 残留旧品牌名「通义灵码」×3

- **位置**：
  1. 正文 L40：「Qoder CN 是阿里出品，**更名前叫通义灵码**，官网 qoder.aliyun.com…」
  2. 正文 L42 锚文本：「…研究过[**通义灵码**（现 Qoder CN）的免费额度]…」
  3. 渲染页相关阅读锚文本（由 frontmatter internal_links 生成）：「**通义灵码**（现 Qoder CN）的免费额度」
- **问题**：通义灵码已于 2026-05-20 正式更名 Qoder CN。按批次红线规则「free-ai-code-completion-tools 应使用 Qoder CN 新名，若残留『通义灵码』即 P0」，正文/锚文本三处残留即命中 P0。
- **说明（性质判断）**：三处均为「更名说明/历史指代」性质的过渡表述（产品当前品牌名 Qoder CN 在 lede、H2、正文已全部正确使用），并非把旧名当现行品牌名使用，误导风险低；但红线规则按字面执行，须处理。
- **修复**（约 2 分钟）：
  - L40 改为「Qoder CN 是阿里出品的智能编码助手，官网以 docs.qoder.cn 为准」；
  - L42 与相关阅读锚文本改为「**Qoder CN 的免费额度**」，仍链 tongyi-lingma-review.html。
  - 若确需保留「原通义灵码」历史说明，请先征得 team-lead 豁免；按当前规则默认**全量去除旧名**。

### P1 — 建议修复（影响外链可信度，2 项 + 1 项增强）

#### P1-1：free-ai-code-completion-tools 外链域名失效 — `qoder.aliyun.com`（DNS 不存在）

- **实测**：`nslookup qoder.aliyun.com` → Non-existent domain；WebFetch 两次均失败。官方入口为 **qoder.com.cn**（阿里云运营的 Qoder CN 全家桶官网）、**docs.qoder.cn**（官方文档）、help.aliyun.com/zh/lingma。
- **修复**：正文 L40「官网 qoder.aliyun.com」及 L42 外链 `https://qoder.aliyun.com/` 改为 `https://docs.qoder.cn/`（或 `https://qoder.com.cn/`）。渲染页需重新构建。

#### P1-2：ai-privacy-data-safety 外链失效 — gov.cn《个人信息保护法》链接跳首页

- **实测**：`https://www.gov.cn/xinwen/2021-08/20/content_5632486.htm` 打开后回落 gov.cn 首页（内容页已下线/迁移）。
- **修复**：替换为网信办官方全文 `https://www.cac.gov.cn/2021-08/20/c_1631050028355286.htm`（已验证有效）。

#### P1-3：what-is-token-ai 对 trustoken.cn 仅泛化警示、未点名（增强项）

- **现状**：结尾已警示「别信网上那些『Token 充值、倒卖、理财』平台，Token 只是计量单位，任何交易平台都不可信」，实体警示成立 ✅，但未点名具体域名。
- **建议**：与本篇选题 brief 及 grammarly 篇点名「grammarlycn.cn」的做法对齐，在结尾句补点 `trustoken.cn` 等具体域名（如「trustoken.cn 这类『Token 交易平台』都是倒卖/理财炒作，别充值」）。

### P2 — 可不处理（优化细节）

- **P2-1 密度系统性略低于理想 1%**（6/10 篇 <1.0%：free-ai-code 0.82、privacy 0.89、token 0.90、id-photo 0.92、copyright 0.92、avatar 0.99）。每篇在结论/提示词段自然 +1~2 次主词即可进入 1% 舒适区。
- **P2-2 H2 含主词均为 1/5**（最低要求满足，理想 2 未达；与第 9 批一致，非阻塞）。
- **P2-3 外链数偏少**：ai-travel-planning-guide、ai-content-copyright-cn 各仅 1 条外链（均为官方/权威，无质量问题；批 9 标准为 2+，可后续补 1 条同主题官方源）。
- **P2-4 主词书写带空格 vs frontmatter 无空格**：正文普遍写「AI 做旅行攻略」「Token 是什么意思」（带空格），primary_keyword 为「ai做旅行攻略」「token是什么意思」（无空格）。搜索引擎视为等价（规范化命中正常），但用精确字符串统计工具会得到 0 次，建议工具统计统一用规范化口径。

---

## 四、Meta 元素优化建议

> **本批题宽 10/10（54–62）、述宽 10/10（146–159）全部合格，且主词均入 Meta Title/Description。按「只给不合格项」原则，本批无必改项。**

| 文章 | 题宽 | 述宽 | 结论 |
|------|------|------|------|
| grammarly-free-alternatives | 56 ✅ | 146 ✅ | 合格 |
| free-ai-code-completion-tools | 54 ✅ | 154 ✅ | 合格（注意：修复 P0/P1 时勿改宽度） |
| ai-id-photo-tutorial | 62 ✅ | 151 ✅ | 合格（题宽 62 已接近上限，改稿勿再加字） |
| ai-avatar-generation-guide | 56 ✅ | 159 ✅ | 合格 |
| ai-audiobook-guide | 54 ✅ | 150 ✅ | 合格 |
| ai-travel-planning-guide | 56 ✅ | 157 ✅ | 合格 |
| what-is-token-ai | 60 ✅ | 150 ✅ | 合格 |
| what-is-prompt-engineering | 54 ✅ | 150 ✅ | 合格 |
| ai-content-copyright-cn | 59 ✅ | 157 ✅ | 合格 |
| ai-privacy-data-safety | 56 ✅ | 150 ✅ | 合格 |

---

## 五、精选摘要捕获机会

全批 10/10 均为「结论前置 + 直答段 + 关键要点」结构，精选摘要条件已具备，无需改动。重点机会：

| 文章 | 摘要类型 | 现状 | 优先级 |
|------|---------|------|--------|
| grammarly-free-alternatives | List/Compare | 首 H2「先分清两种需求」直答 + 四场景对照表 + 仿冒警示 | 高 |
| free-ai-code-completion-tools | List | 「国内选 Qoder CN，国际选 Codeium」直答 + 关键要点 + 测试提示词 | 高 |
| ai-id-photo-tutorial | HowTo | 边界前置 + 三步流程 + 尺寸表 + 自查清单 | 高 |
| ai-avatar-generation-guide | HowTo | 可复制提示词 ×3 组 + 公式 | 高 |
| ai-audiobook-guide | HowTo | 两套流程 + 口播稿提示词 | 高 |
| ai-travel-planning-guide | HowTo | 五步流程 + 可复制提示词模板 | 高 |
| what-is-token-ai | Definition | 首段「Token 是 AI 处理文字的最小单位」定义直答，定义类摘要机会极佳 | 高 |
| what-is-prompt-engineering | Definition | 首段定义 + 好/差对照示例 | 高 |
| ai-content-copyright-cn | Explain/List | 首段「关键看创造性投入」直答 + 三场景列表 + 自查清单 | 高 |
| ai-privacy-data-safety | List | 六类红线清单 + 三件事自查清单 | 高 |

---

## 六、发布检查清单

### 第十批整体状态

- [x] 主关键词在 H1 / 首 H2 — 10/10 ✅
- [x] 主关键词在前 100 字 — 10/10 ✅
- [x] 主关键词在 1+ 个 H2 标题 — 10/10 ✅（理想 2 仅 0 篇，P2-2）
- [ ] 关键词密度 ≥1.0%（1–2% 目标下限） — 4/10 ✅（6 篇偏低，P2-1）
- [x] 3–5+ 正文内链，无断链 — 10/10 ✅（渲染页 4–10 条/篇）
- [x] 外链为官方/权威域名 — 8/10 ✅（2 篇含失效域名，P1-1/P1-2）
- [x] Meta Title 52–64 显示宽含关键词 — 10/10 ✅
- [x] Meta Description 145–162 显示宽含关键词和 CTA — 10/10 ✅
- [x] 正文字数达标（按 article_type 分档） — 10/10 ✅
- [x] 正确 H1/H2/H3 层级 — 10/10 ✅（H2 均 5 个，无跳级）
- [x] 结论有明确 CTA — 10/10 ✅
- [ ] 诚信红线（无 P0） — **9/10 ✅（1 篇 P0，P0-1）**
- [x] 禁词「实测/待核实/TODO」 — 10/10 ✅
- [x] 仿冒镜像未链入 — 10/10 ✅（grammarlycn.cn 为警示性点名，非链接）
- [x] 法律话题软表述 + 法条数字准确 — 2/2 ✅（标识办法 2025-09-01 施行、暂行办法义务表述、无编造法条号）
- [x] 无断链（站内） — 10/10 ✅
- [x] ID 与选题总表一致 — 10/10 ✅（028/033/060/062/069/075/082/084/095/097）

### 逐篇发布状态

| 文章 | 状态 |
|------|------|
| grammarly-free-alternatives | ✅ 可发布 |
| free-ai-code-completion-tools | ❌ **P0 待修复**（通义灵码残留 ×3 + 外链 qoder.aliyun.com 失效） |
| ai-id-photo-tutorial | ✅ 可发布（密度 0.92% 临界，P2） |
| ai-avatar-generation-guide | ✅ 可发布（密度 0.99% 临界，P2） |
| ai-audiobook-guide | ✅ 可发布 |
| ai-travel-planning-guide | ✅ 可发布（外链 1 条偏少，P2） |
| what-is-token-ai | ✅ 可发布（建议 P1-3 点名 trustoken.cn） |
| what-is-prompt-engineering | ✅ 可发布 |
| ai-content-copyright-cn | ✅ 可发布（外链 1 条偏少，P2） |
| ai-privacy-data-safety | ⚠️ 建议修复 P1-2（gov.cn 个保法链接失效）后发布 |

---

## 七、发布建议

### 状态：❌ Needs Revision（1 个 P0 阻塞整批合格）

**理由**：第 10 批整体质量延续第 9 批水准——Meta 全批合格、前 100 字全批覆盖、精选摘要结构全批优良、法律话题软表述与法条数字准确、仿冒镜像零链入；但 **free-ai-code-completion-tools 残留旧品牌名「通义灵码」×3，触发批次 P0 红线**，同时该篇外链 `qoder.aliyun.com` 为不存在域名。按「无 P0 且综合 ≥70 才算合格」标准，本批暂判**不合格**。

### 预估修复时间

| 问题 | 位置 | 预估 |
|------|------|------|
| P0-1 通义灵码残留 ×3 | free-ai-code-completion-tools（L40/L42/锚文本） | 2 分钟 |
| P1-1 外链 qoder.aliyun.com → docs.qoder.cn | free-ai-code-completion-tools（L40/L42） | 1 分钟 |
| P1-2 外链 gov.cn 个保法 → cac.gov.cn | ai-privacy-data-safety（法律义务段） | 1 分钟 |
| P1-3 点名 trustoken.cn（可选） | what-is-token-ai 结尾 | 1 分钟 |
| **合计** | 3 处文件 | **约 5 分钟**（改后重跑构建 + qa_check 确认 0 FAIL） |

### 复评标准

修复 P0-1（+P1-1/P1-2）并重新构建上线后，本批即可转为 **✅ Ready to Publish**（预估复评综合 ≈87/100）。

---

## 附录 A：本批特别关注项核验

| 关注项 | 结论 |
|--------|------|
| grammarly-free-alternatives：警示 grammarlycn.cn 仿冒站 | ✅ 正文 2 处点名警示（关键要点 + 尾段），只认 grammarly.com 官方；外链 grammarly.com + languagetool.org 均为官方，无仿冒链入 |
| free-ai-code-completion-tools：品牌名用 Qoder CN 新名 | ⚠️ **P0**——lede/H2/正文当前品牌名均为 Qoder CN 正确，但残留旧名「通义灵码」×3（更名说明/锚文本），触发红线 |
| free-ai-code-completion-tools：警示破解版/共享账号 | ✅ 关键要点 + 阿凯封号案例 + 尾段双重警示，到位 |
| what-is-token-ai：回避禁词「上下文窗口」 | ✅ 全篇 0 次「上下文窗口」；用「记性空间」「AI 一次能记住多少字」替代；内链锚文本用「AI 为什么会忘事」 |
| what-is-token-ai：警示 trustoken.cn | ⚠️ 泛化警示成立（「Token 充值、倒卖、理财平台都不可信」），未点名具体域名 → P1-3 建议补点 |
| ai-content-copyright-cn：软表述「以官方解释为准」 | ✅ 全文 5 处「以官方解释为准/以司法机关和官方解释为准」；《人工智能生成合成内容标识办法》链接有效，2025-09-01 施行日期与官网原文一致，无编造法条数字 |
| ai-privacy-data-safety：软表述 + gov.cn/cac.gov.cn 有效 + 无编造法条数字 | ✅ 软表述到位；cac.gov.cn 暂行办法链接有效；法条义务描述与《暂行办法》第十一条一致；⚠️ 但 gov.cn《个人信息保护法》链接已失效（P1-2），需替换 |

## 附录 B：外链域名核验明细（第 10 批 16 条）

| 域名 | 文章 | 性质 | 状态 |
|------|------|------|------|
| www.grammarly.com | grammarly | 官方 | ✅ |
| languagetool.org | grammarly | 官方 | ✅ |
| qoder.aliyun.com | free-ai-code | 声称官方 | ❌ DNS 不存在（P1-1） |
| codeium.com | free-ai-code | 官方 | ✅ |
| www.meitu.com | ai-id-photo | 官方 | ✅ |
| www.gov.cn | ai-id-photo | 政务权威 | ✅（通用首页） |
| jimeng.jianying.com | ai-avatar | 官方 | ✅ |
| www.doubao.com | ai-avatar | 官方 | ✅ |
| www.xfyun.cn | ai-audiobook | 官方 | ✅ |
| cloud.baidu.com | ai-audiobook | 官方 | ✅ |
| www.12306.cn | ai-travel | 官方 | ✅ |
| platform.openai.com/tokenizer | token | 官方 | ✅ |
| help.openai.com | token | 官方 | ✅ |
| help.openai.com / docs.anthropic.com | prompt | 官方 | ✅ |
| www.gov.cn（标识办法） | copyright | 政务权威 | ✅（已验证原文） |
| www.cac.gov.cn / www.gov.cn（个保法） | privacy | 政务权威 | ✅ / ❌ 个保法链接失效（P1-2） |

---

*报告生成：2026-08-06 CST | 审计工具：seo-optimizer-3 人工审计 + 量化脚本（规范化密度/前100字/H2/Meta宽度/链接/红线全量扫描，drafts 与渲染 HTML 双重核验）+ DNS/WebFetch 外链实测*
