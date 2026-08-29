#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关键词密度自动优化工具
========================
用途：批量分析并优化文章的 primary_keyword 密度
策略：在结论段、提示词段自然插入关键词变体

用法：
    python optimize_keyword_density.py --dry-run      # 只查看不修改
    python optimize_keyword_density.py                 # 执行优化
    python optimize_keyword_density.py --slug x,y      # 指定文章
"""

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DRAFTS_DIR = ROOT / "drafts"
TARGET_DENSITY = 0.9  # 目标密度（%）


def cjk_count(text):
    """统计中文字符数"""
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def parse_front_matter(content):
    """解析 front-matter，返回 (fm_dict, body)"""
    if not content.lstrip().startswith("---"):
        return {}, content
    
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    
    fm_raw = content[3:end].strip()
    body = content[end + 4:].lstrip("\n")
    
    fm = {}
    current_list = None
    current_item = None
    
    for line in fm_raw.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        s = line.strip()
        
        if indent == 0:
            key, _, val = s.partition(":")
            key, val = key.strip(), val.strip()
            if val == "":
                current_list = []
                fm[key] = current_list
                current_item = None
            else:
                fm[key] = val
                current_list = None
                current_item = None
        else:
            if current_list is None:
                continue
            if s.startswith("- "):
                current_item = {}
                current_list.append(current_item)
                s = s[2:].strip()
                if s:
                    k, _, v = s.partition(":")
                    current_item[k.strip()] = v.strip()
            elif current_item is not None:
                k, _, v = s.partition(":")
                current_item[k.strip()] = v.strip()
    
    return fm, body


def find_optimal_insertion_points(body, keyword, current_count, target_count):
    """
    找到最佳的关键词插入位置
    策略：
    1. 结论段（最后 20% 内容）
    2. 提示词块附近
    3. H2 标题后首句
    """
    insertions = []
    
    # 1. 找结论段（最后 20% 的内容）
    lines = body.split("\n")
    total_lines = len(lines)
    conclusion_start = max(0, total_lines - int(total_lines * 0.2))
    
    # 2. 找现有 H2 标题
    h2_indices = [i for i, l in enumerate(lines) if l.startswith("## ")]
    
    # 3. 找提示词块
    prompt_indices = [i for i, l in enumerate(lines) if "```" in l and ("提示词" in l or "prompt" in l.lower())]
    
    # 生成候选位置
    candidates = []
    
    # 优先级 1：结论段的首个空行或段落开头
    for i in range(conclusion_start, min(conclusion_start + 10, total_lines)):
        if lines[i].strip() == "" or lines[i].startswith("## "):
            candidates.append(("结论段", i, lines[i]))
    
    # 优先级 2：H2 标题后的第一个非空段落
    for idx in h2_indices[-3:]:  # 只看最后 3 个 H2
        for j in range(idx + 1, min(idx + 5, total_lines)):
            if lines[j].strip() and not lines[j].startswith("#"):
                candidates.append(("H2 后", j, lines[j]))
                break
    
    # 优先级 3：提示词块前后
    for idx in prompt_indices[-2:]:  # 只看最后 2 个
        if idx > 0:
            candidates.append(("提示词前", idx - 1, lines[idx - 1]))
        if idx + 1 < total_lines:
            candidates.append(("提示词后", idx + 1, lines[idx + 1]))
    
    return candidates[:5]  # 返回前 5 个最佳位置


def generate_insertion_text(keyword, context_line, position_type):
    """根据上下文生成自然的关键词插入文本"""
    # 关键词变体
    variants = [
        keyword,
        f"关于{keyword.split()[0] if ' ' in keyword else keyword}",
        f"{keyword}的技巧",
        f"掌握{keyword}",
    ]
    
    # 根据位置类型选择合适的插入方式
    if position_type == "结论段":
        # 在结论段自然融入
        template = f"\n> 提示：掌握{keyword.split()[0] if ' ' in keyword else keyword}的关键在于多实践，别怕犯错。"
        return template
    
    elif position_type == "H2 后":
        # 在 H2 后的首句补充
        if context_line.strip().endswith("。"):
            return f"\n{keyword}是这套方法的核心，建议在实操中反复验证。"
        else:
            return f"\n（{keyword}的最佳实践见上文）"
    
    elif position_type == "提示词前" or position_type == "提示词后":
        # 在提示词块附近补充说明
        return f"\n💡 **提示**：使用{keyword}时，记得先明确你的具体场景。"
    
    return f"\n*补充：{keyword}的详细用法请参考上文。"


def optimize_article(draft_path, dry_run=False):
    """优化单篇文章的关键词密度"""
    slug = draft_path.stem
    print(f"\n{'='*60}")
    print(f"📄 {slug}")
    print(f"{'='*60}")
    
    with open(draft_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析 front-matter
    fm, body = parse_front_matter(content)
    keyword = fm.get('primary_keyword', '').strip()
    
    if not keyword:
        print(f"   ⚠️ 缺少 primary_keyword，跳过")
        return False
    
    # 计算当前密度
    clean_body = re.sub(r'```[^`]*```', '', body)
    clean_body = re.sub(r'~{3}[^~]*~{3}', '', clean_body)
    body_cjk = cjk_count(clean_body)
    
    # 精确匹配（不区分大小写，忽略空格差异）
    kw_normalized = re.sub(r'\s+', '', keyword.lower())
    body_normalized = re.sub(r'\s+', '', body.lower())
    kw_count = len(re.findall(re.escape(kw_normalized), body_normalized))
    density = (kw_count / body_cjk * 100) if body_cjk > 0 else 0
    
    print(f"   关键词: \"{keyword}\"")
    print(f"   正文字数: {body_cjk}")
    print(f"   出现次数: {kw_count}")
    print(f"   当前密度: {density:.2f}%")
    
    if density >= TARGET_DENSITY:
        print(f"   ✅ 已达标，无需优化")
        return True
    
    # 计算需要补充的次数
    target_count = int(TARGET_DENSITY * body_cjk / 100)
    needed = target_count - kw_count
    
    print(f"   目标密度: {TARGET_DENSITY}%")
    print(f"   需补充: +{needed} 次")
    
    # 找到插入位置
    candidates = find_optimal_insertion_points(body, keyword, kw_count, target_count)
    
    if not candidates:
        print(f"   ⚠️ 未找到合适的插入位置")
        return False
    
    # 生成优化建议
    print(f"\n   📝 建议插入位置：")
    for i, (pos_type, line_idx, line_text) in enumerate(candidates[:3]):
        preview = line_text.strip()[:50] + "..." if len(line_text) > 50 else line_text.strip()
        print(f"     {i+1}. [{pos_type}] 行 {line_idx}: {preview}")
    
    if dry_run:
        print(f"\n   💡 --dry-run 模式：未实际修改文件")
        return True
    
    # 执行优化（简单版本：在结论段添加提示）
    lines = body.split("\n")
    insertions = []
    
    # 在结论段添加 1-2 个自然插入
    conclusion_start = max(0, len(lines) - int(len(lines) * 0.2))
    inserted = 0
    
    for i in range(conclusion_start, len(lines) - 1):
        if inserted >= min(needed, 3):  # 最多插入 3 次
            break
        if lines[i].strip() == "" and i > 0:
            # 找到空行，插入优化文本
            insert_text = generate_insertion_text(keyword, lines[i-1], "结论段")
            lines.insert(i, insert_text)
            inserted += 1
    
    # 重新组合
    new_body = "\n".join(lines)
    new_content = content.replace(body, new_body)
    
    if not dry_run:
        with open(draft_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"\n   ✅ 已优化，插入 {inserted} 处")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="关键词密度优化工具")
    parser.add_argument("--dry-run", action="store_true", help="只查看不修改")
    parser.add_argument("--slug", type=str, help="指定优化的文章 slug（逗号分隔）")
    args = parser.parse_args()
    
    print("="*60)
    print("LearnTide 关键词密度优化工具")
    print("="*60)
    
    if args.slug:
        # 指定文章
        slugs = [s.strip() for s in args.slug.split(",")]
        draft_paths = [DRAFTS_DIR / f"{s}.md" for s in slugs]
    else:
        # 全部文章
        draft_paths = list(DRAFTS_DIR.glob("*.md"))
    
    print(f"\n模式: {'--dry-run' if args.dry_run else '执行优化'}")
    print(f"待处理: {len(draft_paths)} 篇\n")
    
    results = []
    for draft_path in sorted(draft_paths):
        try:
            success = optimize_article(draft_path, dry_run=args.dry_run)
            results.append((draft_path.name, success))
        except Exception as e:
            print(f"\n   ❌ 错误: {e}")
            results.append((draft_path.name, False))
    
    # 汇总
    print(f"\n{'='*60}")
    print("执行汇总")
    print(f"{'='*60}")
    ok = sum(1 for _, s in results if s)
    print(f"处理: {len(results)} 篇")
    print(f"成功: {ok} 篇")
    print(f"失败: {len(results) - ok} 篇")


if __name__ == "__main__":
    main()
