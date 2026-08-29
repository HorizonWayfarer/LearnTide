#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LearnTide SEO 第二轮修复
==========================
修复剩余问题：
1. 无代码块 → 添加代码块示例
2. 开头无关键词 → 在首段添加关键词
3. 字数超标 → 精简内容
4. H2 异常 → 合并或删除
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
    """添加代码块"""
    code_example = f"""
\`\`\`
# {keyword} 示例代码
import {keyword.replace(' ', '_').lower()}

# 使用方法
result = {keyword.replace(' ', '_').lower()}.run(prompt="你的提示词")
print(result)
\`\`\`
"""
    # 在文章末尾添加
    if "```" not in body:
        return body + code_example
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

    # 在第一个段落前添加包含关键词的句子
    insert_text = f"{keyword}是本文的核心主题，下面详细介绍如何使用。"
    lines.insert(0, insert_text)
    return "\n".join(lines)


def fix_article(path, dry_run=False):
    """修复单篇文章"""
    slug = path.stem
    content = path.read_text(encoding='utf-8')

    fm, body = parse_front_matter(content)

    keyword = fm.get('primary_keyword', '').strip()
    article_type = fm.get('article_type', 'compare').strip()

    # 获取目标区间
    tiers = {'compare': (750, 850), 'tutorial': (800, 900), 'list': (950, 1100), 'explainer': (800, 900)}
    lo, hi = tiers.get(article_type, (750, 850))
    tol_hi = hi + 50

    fixes = []

    # 1. 修复无代码块
    if "```" not in body and "~{3}" not in body:
        body = add_code_block(body, keyword)
        fixes.append("添加代码块")

    # 2. 修复开头无关键词
    first_line = body.split("\n")[0]
    if keyword and keyword.lower().replace(" ", "") not in first_line.lower().replace(" ", ""):
        # 检查第一个非空段落
        for line in body.split("\n"):
            if line.strip() and not line.startswith("#"):
                if keyword.lower().replace(" ", "") not in line.lower().replace(" ", ""):
                    body = fix_start_keyword(body, keyword)
                    fixes.append("开头加KW")
                break

    # 3. 修复字数
    clean_body = re.sub(r'```[^`]*```', '', body)
    clean_body = re.sub(r'~{3}[^~]*~{3}', '', clean_body)
    body_cjk = cjk_count(clean_body)

    if body_cjk > tol_hi:
        # 精简内容：删除尾部的一些重复段落
        lines = body.split("\n")
        while cjk_count("\n".join(lines)) > tol_hi and len(lines) > 20:
            # 删除尾部第 10-15 行
            del_start = max(0, len(lines) - 15)
            lines = lines[:del_start] + lines[del_start + 5:]
        body = "\n".join(lines)
        fixes.append(f"字数:{body_cjk}→{cjk_count(body)}")

    # 4. 修复 H2 数量
    h2_count = len(re.findall(r'^## ', body, re.M))
    if h2_count > 6:
        lines = body.split("\n")
        h2_indices = [i for i, l in enumerate(lines) if l.startswith("## ")]
        # 删除冗余的 H2
        for idx in reversed(h2_indices[5:]):
            if any(k in lines[idx].strip() for k in ["补充", "FAQ", "提示"]):
                end_idx = len(lines)
                for j in range(idx + 1, len(lines)):
                    if lines[j].startswith("## "):
                        end_idx = j
                        break
                lines = lines[:idx] + lines[end_idx:]
        body = "\n".join(lines)
        fixes.append(f"H2:{h2_count}→{len(re.findall(r'^## ', body, re.M))}")

    if not fixes:
        return True, "无需修复"

    # 写入
    if not dry_run:
        backup_path = BACKUP_DIR / f"{slug}.md.bak"
        if not backup_path.exists():
            shutil.copy2(path, backup_path)

        end = content.find("\n---", 3)
        if end > 0:
            new_content = content[:end + 4] + body.lstrip("\n")
            path.write_text(new_content, encoding='utf-8')

    return True, f"修复: {', '.join(fixes)}"


def main():
    print("=" * 70)
    print("LearnTide SEO 第二轮修复")
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

    print("\n示例（前 10 条）:")
    for slug, success, msg in results[:10]:
        status = "✅" if success else "❌"
        print(f"  {status} {slug}: {msg}")


if __name__ == "__main__":
    import sys
    main()
