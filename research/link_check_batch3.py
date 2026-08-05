# -*- coding: utf-8 -*-
import re, os, subprocess

online = set(f[:-3] for f in os.listdir("drafts") if f.endswith(".md"))

with open("research/brief-learntide-100-2026-08-04.md", encoding="utf-8") as f:
    sm = f.read()
planned = set()
for line in sm.split("\n"):
    cells = [c.strip() for c in line.split("|")]
    if len(cells) >= 10 and re.fullmatch(r"\d{3}", cells[1] or ""):
        s = cells[8]
        if re.fullmatch(r"[a-z0-9-]+", s or ""):
            planned.add(s)

batch3 = ["tongyi-qianwen-review","claude-free-tier-limits","ai-voice-tools-compare","ai-coding-assistants-compare","notebooklm-review-guide","ai-wechat-article-writing","notebooklm-tutorial-cn","midjourney-prompt-tips","what-is-ai-agent","ai-trends-2026"]

print("=== 逐篇内链审核 ===")
for slug in batch3:
    c = open("drafts/%s.md" % slug, encoding="utf-8").read()
    m = re.search(r"^---\n(.*?)\n---", c, re.S)
    fm = m.group(1) if m else ""
    links = re.findall(r"slug: ([a-z0-9-]+)", fm)
    paths = re.findall(r"path: ([a-z0-9./-]+)", fm)
    issues = []
    prelinks = []
    for t in links:
        if t in online:
            continue
        if t in planned:
            prelinks.append(t)
            continue
        issues.append("坏链: " + t)
    for t in paths:
        if t.startswith("../"):
            base = t[3:]
        elif t.endswith(".html"):
            base = t
        else:
            continue
        if not os.path.isfile(base) and not os.path.isfile("articles/"+base):
            issues.append("path 不存在: " + t)
    print("  %-30s 已上线链 %d 预埋 %d %s" % (slug, len(links)-len(prelinks), len(prelinks), "!! "+"; ".join(issues) if issues else ""))

print("\n=== 正文内链 ===")
body_issues = []
for slug in batch3:
    c = open("drafts/%s.md" % slug, encoding="utf-8").read()
    body = c.split("---\n\n", 1)[-1] if "---\n\n" in c else c
    for href in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", body):
        tgt = href[1].split("#")[0].split("?")[0].strip()
        if tgt.startswith(("http://", "https://")):
            continue
        tgt_slug = tgt.replace(".html", "")
        if tgt_slug in online:
            continue
        if tgt.startswith("../") and os.path.isfile(tgt[3:]):
            continue
        body_issues.append((slug, tgt, tgt_slug))
print("  指向未上线页:", body_issues if body_issues else "无")

print("\n=== tools.html 配音工具 ===")
th = open("tools.html", encoding="utf-8").read()
cats = set(re.findall(r'"c":"([^"]+)"', th))
print("  当前分类:", cats)
audio_tools = ["剪映", "魔音工坊", "讯飞配音", "腾讯智影", "Suno", "ElevenLabs"]
found = [t for t in audio_tools if t in th]
print("  已收录:", found)
missing = [t for t in audio_tools if t not in th]
print("  未收录:", missing)

print("\n=== 孤岛健康度 ===")
r = subprocess.run(["C:/Users/hwc18/.workbuddy/binaries/python/versions/3.13.12/python.exe", "build_articles.py"], capture_output=True, text=True)
for line in r.stdout.split("\n"):
    if "孤岛" in line:
        print("  " + line.strip())
print("\n完成")