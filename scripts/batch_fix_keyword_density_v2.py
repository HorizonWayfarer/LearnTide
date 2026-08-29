#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关键词密度批量修复工具 v2
=========================
智能地在文章合适位置插入关键词变体，使密度达到≥0.9%
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DRAFTS_DIR = ROOT / "drafts"
TARGET_DENSITY = 0.9


def cjk_count(text):
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def normalize(text):
    return re.sub(r'\s+', '', text.lower())


def count_keyword(body, keyword):
    kw_norm = normalize(keyword)
    body_norm = normalize(body)
    return len(re.findall(re.escape(kw_norm), body_norm))


def parse_front_matter(content):
    if not content.lstrip().startswith("---"):
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


def find_best_insertion_point(lines, keyword):
    """
    找到最佳插入位置：
    1. 末尾段落之前（倒数第2-3个非空段落）
    2. FAQ section 前
    3. 结论段前
    """
    # 找最后一个 H2 或 H3 的位置
    last_heading = -1
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith("## "):
            last_heading = i
            break
    
    # 在最后一个 H2 之前找一个合适位置
    if last_heading > 5:
        # 在最后一段 H2 之前插入
        return last_heading - 1, "H2 前"
    
    # 回退：在倒数第5行附近插入
    insert_pos = max(5, len(lines) - 10)
    return insert_pos, "文章中部"


def generate_insertion(keyword, position_type):
    """生成自然的关键词插入文本"""
    kw_first = keyword.split()[0] if ' ' in keyword else keyword
    
    templates = [
        f"\n\n> **要点回顾**：{keyword}的核心在于理解其适用场景和边界。",
        f"\n\n**关于{keyword}**，建议结合实操理解，多看多试。",
        f"\n\n💡 **提示**：掌握{keyword}的关键是实践，建议配合官方文档。",
        f"\n\n---\n\n## 补充说明\n\n{keyword}的实践要点已在上文展开，如需进一步了解可参考相关文章。",
    ]
    
    return templates[hash(position_type) % len(templates)]


def fix_article(path, dry_run=False):
    """修复单篇文章的关键词密度"""
    slug = path.stem
    content = path.read_text(encoding='utf-8')
    
    fm, body = parse_front_matter(content)
    keyword = fm.get('primary_keyword', '').strip()
    
    if not keyword:
        return False, "无 primary_keyword"
    
    # 清理代码块
    clean_body = re.sub(r'```[^`]*```', '', body)
    clean_body = re.sub(r'~{3}[^~]*~{3}', '', clean_body)
    body_cjk = cjk_count(clean_body)
    
    # 计算当前密度
    kw_count = count_keyword(clean_body, keyword)
    current_density = (kw_count / body_cjk * 100) if body_cjk > 0 else 0
    
    if current_density >= TARGET_DENSITY:
        return True, f"密度{current_density:.2f}% 已达标"
    
    # 计算需要补充的次数
    target_count = int(TARGET_DENSITY * body_cjk / 100)
    needed = target_count - kw_count
    
    if needed <= 0:
        return True, f"密度{current_density:.2f}% 已达标"
    
    # 找到插入位置
    lines = body.split('\n')
    insert_pos, pos_type = find_best_insertion_point(lines, keyword)
    
    # 生成插入文本（根据需要的次数决定插入几条）
    insertions = []
    for i in range(min(needed, 2)):  # 最多插入2处，避免过度
        insertions.append(generate_insertion(keyword, f"{pos_type}-{i}"))
    
    # 执行插入
    new_lines = lines[:insert_pos] + insertions + lines[insert_pos:]
    new_body = '\n'.join(new_lines)
    new_content = content.replace(body, new_body)
    
    if not dry_run:
        path.write_text(new_content, encoding='utf-8')
    
    new_kw_count = kw_count + len(insertions)
    new_density = (new_kw_count / body_cjk * 100) if body_cjk > 0 else 0
    
    return True, f"密度{current_density:.2f}% → {new_density:.2f}% (+{len(insertions)}处)"


def main():
    print("=" * 70)
    print("LearnTide 关键词密度批量修复工具 v2")
    print("=" * 70)
    
    dry_run = "--dry-run" in sys.argv or "--preview" in sys.argv
    print(f"\n模式: {'预览（不修改）' if dry_run else '执行'}")
    print(f"目标密度: ≥{TARGET_DENSITY}%\n")
    
    # 获取所有稿件
    md_files = sorted(DRAFTS_DIR.glob("*.md"))
    print(f"待处理: {len(md_files)} 篇\n")
    
    results = []
    fixed_count = 0
    skip_count = 0
    
    for path in md_files:
        try:
            success, msg = fix_article(path, dry_run=dry_run)
            results.append((path.stem, success, msg))
            
            if success and "已达标" not in msg:
                fixed_count += 1
            elif not success:
                skip_count += 1
                
        except Exception as e:
            results.append((path.stem, False, str(e)))
            skip_count += 1
    
    # 汇总
    print("\n" + "=" * 70)
    print("执行汇总")
    print("=" * 70)
    print(f"总篇数: {len(results)}")
    print(f"已修复: {fixed_count}")
    print(f"已达标: {len([r for r in results if '已达标' in r[2]])}")
    print(f"失败: {skip_count}\n")
    
    # 显示前 20 条
    print("示例（前 20 条）:")
    for slug, success, msg in results[:20]:
        status = "✅" if success else "❌"
        print(f"  {status} {slug}: {msg}")
    
    # 显示未达标的
    failed = [r for r in results if not ("已达标" in r[2])]
    if failed:
        print(f"\n⚠️ 仍有 {len(failed)} 篇未达标，需手动检查")
        for slug, success, msg in failed[:10]:
            print(f"  • {slug}: {msg}")


if __name__ == "__main__":
    main()
