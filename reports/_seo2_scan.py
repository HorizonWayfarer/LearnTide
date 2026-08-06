# -*- coding: utf-8 -*-
import os, re, io

out = io.StringIO()
ROOT = r"A:/LearnTide"

out.write("=== ROOT LISTING ===\n")
for name in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, name)
    out.write(f"  {'DIR ' if os.path.isdir(p) else 'FILE'} {name}\n")

out.write("\n=== ALL .py FILES (recursive) ===\n")
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        if f.endswith(".py"):
            out.write("  " + os.path.join(dp, f).replace("\\", "/") + "\n")

out.write("\n=== FILES MENTIONING qa_check / build_articles ===\n")
for dp, dn, fn in os.walk(ROOT):
    if "__pycache__" in dp:
        continue
    for f in fn:
        if not f.endswith((".py", ".md", ".json", ".txt", ".yml", ".yaml")):
            continue
        p = os.path.join(dp, f)
        try:
            s = open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        if "qa_check" in s or "build_articles" in s:
            out.write(f"  {p.replace(chr(92),'/')}\n")

open(r"A:/LearnTide/reports/_seo2_scan.txt", "w", encoding="utf-8").write(out.getvalue())
