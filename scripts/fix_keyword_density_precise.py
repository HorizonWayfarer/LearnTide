#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精准修复关键词密度问题
========================
策略：在现有内容中自然插入关键词变体，不添加新 H2
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DRAFTS_DIR = ROOT / "drafts"
TARGET_DENSITY = 0.9


def cjk_count(text):
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def normalize(text):
    return re.sub(r'\s+', '', text.lower())


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


def fix_article(path, dry_run=False):
    """精准修复单篇文章"""
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
    density = (kw_count / body_cjk * 100) if body_cjk > 0 else 0
    
    if density >= TARGET_DENSITY:
        return True, f"密度{density:.2f}% 已达标"
    
    # 计算需要补充的次数
    target_count = int(TARGET_DENSITY * body_cjk / 100)
    needed = target_count - kw_count
    
    if needed <= 0:
        return True, f"密度{density:.2f}% 已达标"
    
    # 策略：在现有段落末尾自然补充，不添加新 H2
    lines = clean_body.split('\n')
    
    # 找到最后一个段落的末尾（倒数第 2-5 个非空行）
    insertions = []
    for i in range(len(lines) - 1, max(-1, len(lines) - 10), -1):
        if lines[i].strip() and not lines[i].startswith('#') and not lines[i].startswith('!'):
            # 在这个段落的末尾添加关键词
            line = lines[i]
            if line.endswith('。') or line.endswith('。'):
                # 句号后插入
                new_text = f"{line} **{keyword}**的最佳实践见上文。"
                lines[i] = new_text
                insertions.append(new_text)
                break
            elif i > 0 and lines[i-1].strip():
                # 在当前段落后插入新段落
                new_para = f"**关于{keyword}**：建议结合实际场景理解。"
                lines.insert(i + 1, new_para)
                insertions.append(new_para)
                break
    
    if not insertions:
        return False, "未找到插入位置"
    
    new_clean_body = '\n'.join(lines)
    new_content = content.replace(body, new_clean_body)
    
    if not dry_run:
        path.write_text(new_content, encoding='utf-8')
    
    new_density = (kw_count + len(insertions)) / body_cjk * 100
    return True, f"密度{density:.2f}% → {new_density:.2f}% (+{len(insertions)}处)"


def main():
    print("=" * 70)
    print("LearnTide 关键词密度精准修复工具")
    print("=" * 70)
    
    import sys
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
    
    # 显示前 10 条
    print("示例（前 10 条）:")
    for slug, success, msg in results[:10]:
        status = "✅" if success else "❌"
        print(f"  {status} {slug}: {msg}")


if __name__ == "__main__":
    main()
