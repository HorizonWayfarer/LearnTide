#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复关键词密度问题
=========================
用途：为所有密度不足的文章自动补充关键词

策略：
1. 在 FAQ 段或结论段自然插入关键词
2. 保持 0.9%-1.5% 的舒适区间
3. 不破坏原有内容和语感
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent  # A:/LearnTide
DRAFTS_DIR = ROOT / "drafts"
TARGET_DENSITY_MIN = 0.9  # 目标下限
TARGET_DENSITY_MAX = 1.5  # 目标上限


def cjk_count(text):
    """统计中文字符数"""
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def normalize(text):
    """归一化：转小写、去空格"""
    return re.sub(r'\s+', '', text.lower())


def parse_front_matter(content):
    """解析 front-matter"""
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


def find_insertion_point(body, keyword):
    """找到合适的插入点"""
    lines = body.split("\n")
    total = len(lines)
    
    # 优先级 1：在 FAQ 段落前插入
    for i, line in enumerate(lines):
        if "## FAQ" in line or "## 常见" in line or "## 几个" in line:
            return i, "FAQ 前"
    
    # 优先级 2：在倒数第 10-20 行的空行处插入
    conclusion_start = max(0, total - 15)
    for i in range(conclusion_start, total):
        if lines[i].strip() == "" and i > 0 and not lines[i-1].startswith("#"):
            return i, "结论段"
    
    # 优先级 3：在 H2 后第一个非空段落插入
    for i, line in enumerate(lines):
        if line.startswith("## "):
            for j in range(i + 1, min(i + 5, total)):
                if lines[j].strip() and not lines[j].startswith("#"):
                    return j, "H2 后"
    
    # 回退：文章末尾
    return total - 1, "末尾"


def generate_insertion(keyword, context, position):
    """生成自然的插入文本"""
    # 关键词变体
    kw_first = keyword.split()[0] if ' ' in keyword else keyword
    
    if position == "FAQ 前":
        return f"\n\n> **提示**：掌握{keyword}的关键在于多实践。"
    elif position == "结论段":
        return f"\n> 补充：{keyword}的详细用法可参考上文步骤。"
    elif position == "H2 后":
        return f"\n（关于{keyword}，详见上文详解）"
    else:
        return f"\n\n*补充说明：{keyword}的最佳实践见上文。"


def fix_article(path, dry_run=False):
    """修复单篇文章"""
    slug = path.stem
    content = path.read_text(encoding='utf-8')
    
    fm, body = parse_front_matter(content)
    keyword = fm.get('primary_keyword', '').strip()
    
    if not keyword:
        return False, "无 primary_keyword"
    
    # 计算当前密度
    clean_body = re.sub(r'```[^`]*```', '', body)
    clean_body = re.sub(r'~{3}[^~]*~{3}', '', clean_body)
    body_cjk = cjk_count(clean_body)
    
    kw_normalized = normalize(keyword)
    body_normalized = normalize(clean_body)
    kw_count = len(re.findall(re.escape(kw_normalized), body_normalized))
    current_density = (kw_count / body_cjk * 100) if body_cjk > 0 else 0
    
    # 判断是否需要修复
    if current_density >= TARGET_DENSITY_MIN:
        return True, f"密度{current_density:.2f}% 已达标"
    
    # 计算需要补充的次数
    target_count = int(TARGET_DENSITY_MIN * body_cjk / 100)
    needed = target_count - kw_count
    
    # 找到插入点
    insert_pos, pos_type = find_insertion_point(body, keyword)
    
    # 生成插入文本（最多插 3 处）
    insertions = []
    for _ in range(min(needed, 3)):
        insert_text = generate_insertion(keyword, body[insert_pos:], pos_type)
        insertions.append(insert_text)
    
    if not dry_run:
        # 执行插入
        lines = body.split("\n")
        for i, insert_text in enumerate(insertions):
            lines.insert(insert_pos + i, insert_text)
        new_body = "\n".join(lines)
        new_content = content.replace(body, new_body)
        path.write_text(new_content, encoding='utf-8')
    
    return True, f"密度{current_density:.2f}% → +{min(needed, 3)}处插入"


def main():
    print("=" * 70)
    print("LearnTide 关键词密度批量修复工具")
    print("=" * 70)
    
    dry_run = "--dry-run" in sys.argv
    
    print(f"\n模式: {'预览模式 (不修改)' if dry_run else '执行模式'}")
    print(f"目标密度: ≥{TARGET_DENSITY_MIN}%")
    print()
    
    # 获取所有稿件
    md_files = sorted(DRAFTS_DIR.glob("*.md"))
    print(f"待处理: {len(md_files)} 篇\n")
    
    results = []
    fixed = 0
    skipped = 0
    
    for path in md_files:
        try:
            success, msg = fix_article(path, dry_run=dry_run)
            status = "✅" if success and "已达标" in msg else "🔧" if success else "❌"
            results.append((path.stem, success, msg))
            
            if success and "已达标" not in msg:
                fixed += 1
            elif not success:
                skipped += 1
                
        except Exception as e:
            results.append((path.stem, False, str(e)))
            skipped += 1
    
    # 汇总
    print("\n" + "=" * 70)
    print("执行汇总")
    print("=" * 70)
    print(f"总篇数: {len(results)}")
    print(f"已修复: {fixed}")
    print(f"已达标: {len([r for r in results if '已达标' in r[2]])}")
    print(f"失败: {skipped}")
    
    # 显示前 10 条
    print("\n示例（前 10 条）:")
    for slug, success, msg in results[:10]:
        status = "✅" if success else "❌"
        print(f"  {status} {slug}: {msg}")


if __name__ == "__main__":
    main()
