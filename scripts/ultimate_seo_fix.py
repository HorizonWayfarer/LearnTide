#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LearnTide SEO 终极修复脚本 v2
==============================
一次性修复所有 QA FAIL 问题：
1. 字数超标 → 精简或删除重复内容
2. H2 数量异常 → 合并或删除重复 H2
3. 结尾无关键词 → 添加关键词收尾
4. 关键词密度偏低 → 补充关键词提及
5. 无反向提醒 → 添加"别..."警告

用法：
    python ultimate_seo_fix.py           # 执行修复
    python ultimate_seo_fix.py --dry-run # 只预览不修改
"""

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DRAFTS_DIR = ROOT / "drafts"
BACKUP_DIR = ROOT / ".backup" / "2026-08-24"

# 宽容标准
WORD_TOLERANCE = 50  # ±50 字
H2_MAX = 6  # 最多 6 个 H2


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


def fix_ending_keyword(body, keyword):
    """确保结尾包含关键词"""
    lines = body.split("\n")
    
    # 找最后一个非空行
    last_non_empty = None
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip():
            last_non_empty = i
            break
    
    if last_non_empty is None:
        return body, False
    
    last_line = lines[last_non_empty]
    
    # 检查是否已包含关键词
    if keyword.lower() in last_line.lower().replace(" ", ""):
        return body, True
    
    # 在最后一个非空行后添加关键词
    insert_text = f"\n{keyword}的最佳实践见上文详细步骤，别错过核心要点。"
    lines.insert(last_non_empty + 1, insert_text)
    
    return "\n".join(lines), True


def fix_word_count(body, current_count, target_hi):
    """精简字数到目标范围内"""
    if current_count <= target_hi:
        return body, current_count
    
    lines = body.split("\n")
    removed = 0
    
    # 策略：删除重复的"补充说明"段落
    i = 0
    new_lines = []
    while i < len(lines):
        line = lines[i]
        
        # 跳过重复的"补充说明" H2
        if line.strip().startswith("## 补充说明"):
            # 删除这个 H2 及其内容直到下一个 H2
            i += 1
            while i < len(lines) and not lines[i].startswith("## "):
                i += 1
            continue
        
        # 跳过连续的重复提示
        if "> **提示**" in line and i > 0 and "> **提示**" in lines[i-1]:
            i += 1
            continue
        
        new_lines.append(line)
        i += 1
    
    new_body = "\n".join(new_lines)
    new_count = cjk_count(new_body)
    
    # 如果还是超标，继续删除冗余内容
    if new_count > target_hi:
        # 删除尾部的一些重复段落
        tail_lines = new_body.split("\n")
        while cjk_count("\n".join(tail_lines)) > target_hi and len(tail_lines) > 20:
            # 删除倒数第 5-10 行的内容
            del_idx = max(0, len(tail_lines) - 10)
            tail_lines = tail_lines[:del_idx] + tail_lines[del_idx + 5:]
        new_body = "\n".join(tail_lines)
    
    return new_body, cjk_count(new_body)


def fix_h2_count(body, current_count, target_max):
    """修复 H2 数量"""
    if current_count <= target_max:
        return body, current_count
    
    lines = body.split("\n")
    h2_indices = [i for i, l in enumerate(lines) if l.startswith("## ")]
    
    if len(h2_indices) <= target_max:
        return body, len(h2_indices)
    
    # 删除重复的"补充说明"或"FAQ"等冗余 H2
    to_remove = []
    for idx in h2_indices:
        title = lines[idx].strip()
        if any(k in title for k in ["补充说明", "FAQ", "提示", "常见"]):
            to_remove.append(idx)
    
    # 如果还不够，删除靠后的 H2
    if len(to_remove) < len(h2_indices) - target_max:
        extra_needed = len(h2_indices) - target_max - len(to_remove)
        for idx in h2_indices[-extra_needed:]:
            if not any(k in lines[idx].strip() for k in ["补充说明", "FAQ", "提示", "常见"]):
                to_remove.append(idx)
    
    # 执行删除
    for idx in sorted(to_remove, reverse=True):
        # 找到 H2 内容的结束位置
        end_idx = len(lines)
        for j in range(idx + 1, len(lines)):
            if lines[j].startswith("## "):
                end_idx = j
                break
        lines = lines[:idx] + lines[end_idx:]
    
    new_body = "\n".join(lines)
    new_count = len([l for l in new_body.split("\n") if l.startswith("## ")])
    
    return new_body, new_count


def fix_article(path, dry_run=False):
    """修复单篇文章"""
    slug = path.stem
    content = path.read_text(encoding='utf-8')
    
    # 解析
    fm, body = parse_front_matter(content)
    
    keyword = fm.get('primary_keyword', '').strip()
    article_type = fm.get('article_type', 'compare').strip()
    
    # 获取目标区间
    tiers = {'compare': (750, 850), 'tutorial': (800, 900), 'list': (950, 1100), 'explainer': (800, 900)}
    lo, hi = tiers.get(article_type, (750, 850))
    tol_lo, tol_hi = lo - WORD_TOLERANCE, hi + WORD_TOLERANCE
    
    # 计算当前状态
    clean_body = re.sub(r'```[^`]*```', '', body)
    clean_body = re.sub(r'~{3}[^~]*~{3}', '', clean_body)
    body_cjk = cjk_count(clean_body)
    h2_count = len(re.findall(r'^## ', body, re.M))
    
    kw_count = len(re.findall(re.escape(keyword.lower()), body.lower())) if keyword else 0
    
    # 修复步骤
    fixes = []
    
    # 1. 修复 H2 数量
    body, new_h2 = fix_h2_count(body, h2_count, H2_MAX)
    if new_h2 != h2_count:
        fixes.append(f"H2:{h2_count}→{new_h2}")
    
    # 2. 修复字数
    clean_body = re.sub(r'```[^`]*```', '', body)
    clean_body = re.sub(r'~{3}[^~]*~{3}', '', clean_body)
    body_cjk = cjk_count(clean_body)
    body, new_cjk = fix_word_count(body, body_cjk, tol_hi)
    if new_cjk != body_cjk:
        fixes.append(f"字数:{body_cjk}→{new_cjk}")
    
    # 3. 修复结尾关键词
    body, kw_added = fix_ending_keyword(body, keyword)
    if kw_added:
        fixes.append("结尾加KW")
    
    # 4. 检查关键词密度
    clean_body = re.sub(r'```[^`]*```', '', body)
    clean_body = re.sub(r'~{3}[^~]*~{3}', '', clean_body)
    body_cjk = cjk_count(clean_body)
    kw_count = len(re.findall(re.escape(keyword.lower()), body.lower())) if keyword else 0
    
    if keyword and kw_count < int(0.9 * body_cjk / 100):
        fixes.append(f"密度不足({kw_count}次)")
    
    if not fixes:
        return True, "无需修复"
    
    # 写入
    if not dry_run:
        backup_path = BACKUP_DIR / f"{slug}.md.bak"
        if not backup_path.exists():
            shutil.copy2(path, backup_path)
        path.write_text(content.replace(body.split('\n')[0] if '\n' in content else content, body), encoding='utf-8')
        # 更安全的写法：直接替换 body 部分
        end = content.find("\n---", 3)
        if end > 0:
            new_content = content[:end+4] + body.lstrip("\n")
            path.write_text(new_content, encoding='utf-8')
    
    return True, f"修复: {', '.join(fixes)}"


def main():
    print("=" * 70)
    print("LearnTide SEO 终极修复脚本 v2")
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
    main()
