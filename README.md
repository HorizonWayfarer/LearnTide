# Learntide · 学习潮汐

> AI 工具 / 教程 / 资讯内容站。靠 SEO 获取自然流量，后续接 Google AdSense 或联盟链接变现。
> 主域名：`learntide.cc.cd`

## 项目定位

- **内容站主线**（首页 / 文章页 / 关于页）+ **工具导航页**（tools.html，32 个真实工具、7 个分类、搜索 + 分类筛选）。
- **视觉基调**：水木浅色——主色 water-blue `#3b82c4`、辅色 wood-green `#5a8a6a`，宁静、清爽、可读性强。
- **技术栈**：纯静态 HTML + CSS + 原生 JS，0 成本、易部署、SEO 友好。后续流量起来再考虑升级到 Astro / Next.js。

## 目录结构

```
Learntide/
├── index.html                       # 首页：简介 + 最新文章 + 栏目入口
├── tools.html                       # AI 工具导航页（数据驱动，见下）
├── about.html                       # 关于页
├── articles/                        # 文章页目录（跨页链接需用 ../ 回退根目录）
├── assets/
│   ├── style.css                    # 全局设计系统（40+ CSS 变量 Token）
│   ├── covers/                      # 文章封面图（jpg / webp）
│   ├── figures/                     # 文章正文配图（jpg / webp）
│   └── fonts/                       # 站点 Web 字体（LXGW WenKai，须提交，否则线上字体 404）
├── scripts/                         # 构建 / QA / 推送等脚本（scripts/autopublish/ 已忽略）
├── sitemap.xml                      # 站点地图（新增页面需同步更新）
├── robots.txt                       # 爬虫规则
├── _headers                         # Cloudflare Pages 缓存策略
├── _redirects                      # Cloudflare Pages 重定向
├── build_articles.py               # 文章构建脚本（md → html）
├── qa_check.py                      # 内容质量检查
├── serve.py                         # 本地静态预览服务器（由你本机启动）
└── learntide-brief.md               # 项目简报（含命理底子与完整策划）
```

## 本地预览

预览服务器需由你本机启动（本项目 AI 只产出代码文件、不负责启动服务器）。

```bash
cd A:\LearnTide
python serve.py                 # 默认 http://127.0.0.1:8000
python serve.py --port 8080     # 换端口
python serve.py --root ./articles  # 只服务某个子目录
```

然后浏览器打开 `http://127.0.0.1:8000/` 即可看到真实版式。

## 如何添加内容

### 1. 加一个 AI 工具（改 tools.html）

工具页由 `tools.html` 里的 `TOOLS` 数组驱动，新增工具只需往数组里加一条对象，无需改 HTML 结构：

```js
{n:"工具名", v:"厂商", d:"一句话真实描述，不夸大不编造", c:"分类", t:["标签"]}
```

- `c`（分类）取值需与现有 7 类一致：对话AI / 图像生成 / 编程助手 / 写作文案 / 音视频 / 商业效率 / 国内专区
- `t`（标签）可选值：`热门` / `免费` / `NEW` / `国内`（可组合，如 `["国内","免费"]`）

### 2. 加一篇新文章

1. 在 `articles/` 目录下新建 `your-slug.html`，复制示例文章 `ai-weekly-report-guide.html` 的结构。
2. **相对路径注意**：子目录页面的跨页链接要用 `../` 回退根目录（如 `../index.html`、`../tools.html`、`../assets/style.css`）；同目录文件（如 `ai-weekly-report-guide.html`）和页内锚点（`#id`）不用加。
3. 填写每篇文章的 `meta description`、`<title>`，并在 `<script type="application/ld+json">` 里更新标题/日期/作者，利于 SEO。
4. 文章正文建议结构：`.lede`（导语）→ `h2`/`h3` 小标题 → `p` 正文；教程中的提示词用 `<pre><code>` 代码块，金句用 `<blockquote>` 引用块。
5. 把新文章链接加到首页 `index.html` 的文章列表，并更新 `sitemap.xml`。

## 部署（GitHub → Cloudflare Pages）

> git 写操作（init / add / commit / push 等）由你本机执行（本项目 AI 只产出文件、不执行 git 写操作）。

```bash
# 首次初始化（仅一次）
cd /d A:\LearnTide
git init
git branch -M main
git remote add origin https://github.com/HorizonWayfarer/LearnTide.git

# 日常更新：绝不 git add . / git add -A，按文件提交
git add articles/ articles.html index.html sitemap.xml assets/ robots.txt _headers _redirects .gitignore README.md
git commit -m "feat: 内容重建 + 仓库清理（字体/忽略规则）"
git push
```

然后在 Cloudflare Pages：

1. 新建项目 → 连接刚 push 的 GitHub 仓库。
2. 构建命令**留空**，输出目录填 **`.`**（站点文件在仓库根）。
3. 在自定义域名里填 `learntide.cc.cd`（DNS / CNAME 已配好，绑定后自动签发 HTTPS）。

仓库地址：<https://github.com/HorizonWayfarer/LearnTide.git>

## 设计系统（速查）

- **颜色 Token**：`--water` / `--water-dark` / `--water-light`（水蓝系）、`--wood` / `--wood-dark` / `--wood-light`（木绿系）、中性灰阶走 Slate（`--text` / `--muted` / `--meta` / `--border`）。除 `#fff`/`#000` 外一律走 Token，禁止硬编码颜色。
- **字体**：`"Noto Sans SC"` + 系统无衬线回退；正文 `line-height: 1.65`。
- **节奏**：section 垂直 padding 48px、卡片 padding 24px、文章段间距 24px、正文 max-width 720px。
- **反模式红线**：禁止 emoji 功能图标（只用内联 SVG）、禁止紫粉渐变、禁止 AI 模板味（无毛玻璃、无标题侧条纹、卡片悬浮不上浮）。
- **图标**：全部内联 SVG，描边风格、viewBox `0 0 16 16`、stroke-width 1.5，未引入任何图标库。

## 后续迭代方向

- 内容积累到 20+ 篇后，做站内搜索、标签系统。
- 流量起来后申请 AdSense / 接入联盟链接（广告位已在页内留好占位框）。
- 可考虑 RSS、newsletter 沉淀私域。
