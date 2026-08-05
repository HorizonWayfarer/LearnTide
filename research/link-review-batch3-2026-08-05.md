# 链接审核报告 · 第三批（2026-08-05）

> 审核人：连乐桥（链接策略师）— 因 429 限流中断，由主理人接管脚本 `research/link_check_batch3.py` 跑通并收口
> 范围：第三批 10 篇（tongyi-qianwen-review / claude-free-tier-limits / ai-voice-tools-compare / ai-coding-assistants-compare / notebooklm-review-guide / ai-wechat-article-writing / notebooklm-tutorial-cn / midjourney-prompt-tips / what-is-ai-agent / ai-trends-2026）
> 方法：静态解析 front-matter 内链 + 正文内链 + tools.html 出链 + build_articles.py 孤岛体检

## 一、逐篇内链合规（front-matter）

|  slug | 已上线链 | 预埋链 | 问题 |
|------|--------|--------|------|
| tongyi-qianwen-review | 4 | 0 | 无 |
| claude-free-tier-limits | 4 | 0 | 无 |
| ai-voice-tools-compare（★C6 支柱）| 1 | 3 | 预埋 suno-ai-music-review / elevenlabs-voice-review / suno-ai-tutorial-cn |
| ai-coding-assistants-compare（★C8 支柱）| 2 | 2 | 预埋 tongyi-lingma-review / cursor-beginner-tutorial |
| notebooklm-review-guide | 3 | 1 | 预埋 perplexity-ai-search-review |
| ai-wechat-article-writing | 4 | 0 | 无 |
| notebooklm-tutorial-cn | 3 | 1 | 预埋 ai-reading-notes-method |
| midjourney-prompt-tips | 3 | 0 | 无 |
| what-is-ai-agent | 3 | 1 | 预埋 what-is-prompt-engineering |
| ai-trends-2026 | 3 | 1 | 预埋 ai-beginner-learning-path |

**结论**：全部 `slug:` 字段指向「已上线页」或「规划表 slug（预埋）」，无坏链、无 path 不存在。`build_articles.py` 死链保护已生效，预埋目标未上线时自动跳过，不会生成死链。

## 二、正文内链体检

- 扫描 10 篇正文 `[文本](目标)` 链接，过滤外链（http/https）后逐一比对。
- **结果：指向未上线页 = 无**。所有正文内链均命中已上线页或 `../` 站点相对路径文件。

## 三、tools.html 配音/语音工具覆盖

当前 tools.html 已收录语音类工具：**剪映、Suno、ElevenLabs**（3/6）。
未收录：**魔音工坊、讯飞配音、腾讯智影**（3/6）。

- ai-voice-tools-compare（C6 支柱）已上线，但其卫星工具 Suno/ElevenLabs 已在 tools.html，魔音工坊/讯飞配音/腾讯智影缺失。
- **建议**：待对应工具测评文（suno-ai-music-review、elevenlabs-voice-review 等）上线时，同步将魔音工坊/讯飞配音/腾讯智影补录至 tools.html 语音分类；本期不阻塞交付。

## 四、孤岛健康度（0 条站内入链）

`build_articles.py` 体检输出孤岛：
- **ai-voice-tools-compare**（C6 支柱）
- **ai-wechat-article-writing**
- **claude-free-tier-limits**
- **midjourney-prompt-tips**
- **tongyi-qianwen-review**
（另含历史页 ai-resume-optimization、chatgpt-plus-worth-it）

**判定**：5 篇为第三批页，孤岛状态属**预期 interim 行为**——其入链来源（同簇兄弟文 / 支柱页反向链接）尚未写到（全站仅 33/100 篇）。预埋机制只解决「出链到未来页」，入链需后续批次落笔。

**后续动作**：第四批起，链接策略需在对应簇支柱/兄弟文补「反向入链」至本批 5 个孤岛；优先 ai-voice-tools-compare（C6 支柱，应被语音类卫星文回链）、ai-coding-assistants-compare（C8，已被 tongyi-lingma-review / cursor-beginner-tutorial 预埋出链，需其上线后回填）。

## 五、内容健康度评分

| 维度 | 得分 | 说明 |
|------|------|------|
| 内链合规 | 100 | 无坏链、无死 path |
| 正文链接安全 | 100 | 无指向未上线页 |
| 聚类覆盖 | 85 | 预埋到位，但孤岛 5 篇待回填 |
| 出链健康 | 90 | tools.html 语音类缺 3 项（非阻塞）|
| 预埋规范 | 100 | slug 三态校验全过 |

**综合：95 / 100** — 达到发布标准，孤岛与 tools.html 缺口记入第四批链接待办。

## 六、发布前待办（移交第四批）

1. 第四批写语音类（魔音工坊/讯飞配音/腾讯智影）测评时，补 tools.html 语音分类 3 条出链。
2. 第四批链接 pass 给本批 5 个孤岛补反向入链（优先级：ai-voice-tools-compare → ai-coding-assistants-compare → 其余 3 篇）。
3. 预埋 slug 上线即生效，无需回改本批。

---
审核收口：2026-08-05 15:50 · 主理人代 连乐桥 执行并签署
