#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LearnTide H2 去重清理脚本
===========================
清理重复添加的 H2 段落（如多个"示例代码"、"使用方法"等）
"""

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
DRAFTS_DIR = ROOT / "drafts"
BACKUP_DIR = ROOT / ".backup" / "2026-08-24"


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


def deduplicate_h2(body):
    """去除重复的 H2 段落"""
    lines = body.split("\n")
    h2_indices = [(i, line) for i, line in enumerate(lines) if line.startswith("## ")]

    # 检测重复的 H2 标题
    duplicate_keywords = ["示例代码", "使用方法", "代码示例", "使用方法示例"]

    # 记录需要删除的 H2 索引范围
    to_remove = []

    for i, (idx, h2_line) in enumerate(h2_indices):
        h2_title = h2_line.replace("## ", "").strip()

        # 检查是否是重复类型
        is_duplicate = False
        for keyword in duplicate_keywords:
            if keyword in h2_title:
                is_duplicate = True
                break

        if is_duplicate:
            # 找到下一个 H2 的位置
            end_idx = len(lines)
            for j in range(idx + 1, len(lines)):
                if lines[j].startswith("## "):
                    end_idx = j
                    break

            # 只保留第一个重复的 H2
            first_occurrence = None
            for prev_idx, prev_line in h2_indices[:i]:
                prev_title = prev_line.replace("## ", "").strip()
                for keyword in duplicate_keywords:
                    if keyword in prev_title:
                        first_occurrence = prev_idx
                        break
                if first_occurrence is not None:
                    break

            if first_occurrence is None or idx > first_occurrence:
                to_remove.append((idx, end_idx))

    # 执行删除（从后往前）
    for start, end in sorted(to_remove, reverse=True):
        lines = lines[:start] + lines[end:]

    return "\n".join(lines)


def fix_article(path, dry_run=False):
    """修复单篇文章的 H2 重复问题"""
    slug = path.stem
    content = path.read_text(encoding='utf-8')

    fm, body = parse_front_matter(content)

    # 统计原始 H2 数量
    original_h2_count = len(re.findall(r'^## ', body, re.M))

    # 执行去重
    new_body = deduplicate_h2(body)

    # 统计新 H2 数量
    new_h2_count = len(re.findall(r'^## ', new_body, re.M))

    if original_h2_count == new_h2_count:
        return True, "无需修复"

    # 写入
    if not dry_run:
        backup_path = BACKUP_DIR / f"{slug}.md.bak"
        if not backup_path.exists():
            shutil.copy2(path, backup_path)

        end = content.find("\n---", 3)
        if end > 0:
            new_content = content[:end + 4] + new_body.lstrip("\n")
            path.write_text(new_content, encoding='utf-8')

    return True, f"H2:{original_h2_count}→{new_h2_count}"


def main():
    print("=" * 70)
    print("LearnTide H2 去重清理")
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
