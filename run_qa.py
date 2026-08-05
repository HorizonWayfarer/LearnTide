# -*- coding: utf-8 -*-
"""以 UTF-8 稳定捕获 qa_check.py 输出，规避 Windows 终端编码问题。
不修改 qa_check.py 本身（艾笔润正在改该文件）。"""
import subprocess, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))
env = dict(os.environ, PYTHONIOENCODING="utf-8")
r = subprocess.run([sys.executable, os.path.join(ROOT, "qa_check.py")],
                   capture_output=True, cwd=ROOT, env=env)
out = (r.stdout + r.returncode.to_bytes(0, "big") + r.stderr)
for enc in ("utf-8", "gbk", "cp936"):
    try:
        text = out.decode(enc)
        break
    except UnicodeDecodeError:
        continue
else:
    text = out.decode("utf-8", "replace")
with open(os.path.join(ROOT, "qa_out.txt"), "w",
          encoding="utf-8", newline="\n") as f:
    f.write(text)
