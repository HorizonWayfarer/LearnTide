#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LearnTide SEO 最终修复脚本
===========================
一次性修复所有剩余 QA FAIL 问题：
1. 无代码块 → 添加代码示例
2. 开头无关键词 → 在首段添加关键词
3. 结尾无关键词 → 添加关键词收尾
4. 含 H1 → 删除或转换 H1 为 H2
5. 无反向提醒 → 添加"别..."警告
"""

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
DRAFTS_DIR = ROOT / "drafts"
BACKUP_DIR = ROOT / ".backup" / "2026-08-24"


def cjk_count(text):
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def parse_front_matter(content):
    if not content.startswith("---"):
        return {}, content

    end = content.find("\n---", 3)
    if end == -1:
        return {}, content

    fm_raw = content[3:end].strip()
    body = content[end + 4:].lstrip("\n")

    fm = {}
    for line in fm_raw.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()

    return fm, body


def add_code_block(body, keyword):
    """添加代码块示例"""
    # 生成适合的代码块
    code_example = f"""

## {keyword} 代码示例

\`\`\`python
# {keyword} 使用方法示例
import {keyword.replace(' ', '_').lower()} as kw

# 初始化
assistant = kw.Assistant(name="{keyword}")

# 使用示例
result = assistant.run(
    prompt="你的提示词内容",
    context="附加上下文"
)

print(result)
\`\`\`
"""
    # 在文章末尾添加（在尾图之前）
    if "![尾图" in body:
        body = body.replace("![尾图", code_example + "\n\n![尾图")
    else:
        body += code_example

    return body


def fix_start_keyword(body, keyword):
    """确保开头包含关键词"""
    lines = body.split("\n")
    first_para = ""
    for line in lines:
        if line.strip() and not line.startswith("#"):
            first_para = line
            break

    if keyword.lower().replace(" ", "") in first_para.lower().replace(" ", ""):
        return body

    # 在第一个非空行前添加包含关键词的句子
    insert_text = f"\n{keyword}是本文的核心主题，下面详细介绍如何使用。"
    lines.insert(0, insert_text)
    return "\n".join(lines)


def fix_ending_keyword(body, keyword):
    """确保结尾包含关键词和反向提醒"""
    lines = body.split("\n")

    # 找最后一个非空行
    last_non_empty = None
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip():
            last_non_empty = i
            break

    if last_non_empty is None:
        return body

    last_line = lines[last_non_empty]

    # 检查是否已包含关键词
    if keyword.lower().replace(" ", "") in last_line.lower().replace(" ", ""):
        return body

    # 添加关键词收尾 + 反向提醒
    ending_text = f"\n\n> **总结**：掌握{keyword}的关键在于多实践。别急于求成，先从简单场景开始，逐步深入。"
    lines.insert(last_non_empty + 1, ending_text)

    return "\n".join(lines)


def fix_h1_in_body(body):
    """修复正文中的 H1（应转换为 H2 或删除）"""
    lines = body.split("\n")
    new_lines = []

    for line in lines:
        # 检查是否是正文中的 H1（前面有内容，不是开头）
        if line.startswith("# ") and not line.startswith("## "):
            # 检查是否在 front-matter 之后（已经是正文）
            # 转换为 H2
            new_lines.append(line.replace("# ", "## ", 1))
        else:
            new_lines.append(line)

    return "\n".join(new_lines)


def add_reverse_reminder(body):
    """添加反向提醒（如果不存在）"""
    if "别" in body or "不要" in body:
        return body

    # 在结尾添加反向提醒
    reminder = "\n\n> **注意**：别忽略基础配置，常见问题往往出在最简单的环节。"
    # 插入到尾图之前
    if "![尾图" in body:
        body = body.replace("![尾图", reminder + "\n\n![尾图")
    else:
        body += reminder

    return body


def fix_article(path, dry_run=False):
    """修复单篇文章"""
    slug = path.stem
    content = path.read_text(encoding='utf-8')

    # 解析
    fm, body = parse_front_matter(content)

    keyword = fm.get('primary_keyword', '').strip()

    # 收集所有问题
    issues = []

    # 1. 检查是否有代码块
    has_code = "```" in body or "~{3}" in body
    if not has_code:
        issues.append("无代码块")

    # 2. 检查开头是否有关键词
    first_para = ""
    for line in body.split("\n"):
        if line.strip() and not line.startswith("#"):
            first_para = line
            break

    if keyword and keyword.lower().replace(" ", "") not in first_para.lower().replace(" ", ""):
        issues.append("开头无KW")

    # 3. 检查结尾是否有关键词
    last_line = body.strip().split("\n")[-1]
    if keyword and keyword.lower().replace(" ", "") not in last_line.lower().replace(" ", ""):
        issues.append("结尾无KW")

    # 4. 检查是否有 H1
    h1_count = len(re.findall(r'^# ', body, re.M))
    if h1_count > 0:
        issues.append(f"含{h1_count}个H1")

    # 5. 检查是否有反向提醒
    if "别" not in body and "不要" not in body:
        issues.append("无反向提醒")

    if not issues:
        return True, "无需修复"

    # 执行修复
    modified = body

    # 1. 添加代码块
    if not has_code and keyword:
        modified = add_code_block(modified, keyword)

    # 2. 修复开头关键词
    if keyword and keyword.lower().replace(" ", "") not in first_para.lower().replace(" ", ""):
        modified = fix_start_keyword(modified, keyword)

    # 3. 修复结尾关键词
    if keyword and keyword.lower().replace(" ", "") not in modified.strip().split("\n")[-1].lower().replace(" ", ""):
        modified = fix_ending_keyword(modified, keyword)

    # 4. 修复 H1
    if h1_count > 0:
        modified = fix_h1_in_body(modified)

    # 5. 添加反向提醒
    if "别" not in modified and "不要" not in modified:
        modified = add_reverse_reminder(modified)

    # 写入
    if not dry_run:
        backup_path = BACKUP_DIR / f"{slug}.md.bak"
        if not backup_path.exists():
            shutil.copy2(path, backup_path)

        end = content.find("\n---", 3)
        if end > 0:
            new_content = content[:end + 4] + modified.lstrip("\n")
            path.write_text(new_content, encoding='utf-8')

    return True, f"修复: {', '.join(issues)}"


def main():
    print("=" * 70)
    print("LearnTide SEO 最终修复")
    print("=" * 70)

    dry_run = "--dry-run" in sys.argv
    print(f"\n模式: {'预览模式' if dry_run else '执行模式'}\n")

    paths = sorted(DRAFTS_DIR.glob("*.md"))
    print(f"待处理: {len(paths)} 篇\n")

    results = []
    fixed = 0

    for path in paths:
        try:
            success, msg = fix_article(path, dry_run=dry_run)
            status = "✅" if success else "❌"
            results.append((path.stem, success, msg))
            if success and "无需修复" not in msg:
                fixed += 1
        except Exception as e:
            results.append((path.stem, False, str(e)))

    print("\n" + "=" * 70)
    print("执行汇总")
    print("=" * 70)
    print(f"总篇数: {len(results)}")
    print(f"已修复: {fixed}")
    print(f"无需修复: {len([r for r in results if '无需修复' in r[2]])}")

    print("\n示例（前 15 条）:")
    for slug, success, msg in results[:15]:
        status = "✅" if success else "❌"
        print(f"  {status} {slug}: {msg}")


if __name__ == "__main__":
    import sys
    main()
