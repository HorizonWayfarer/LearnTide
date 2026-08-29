#!/usr/bin/env python3
"""
表格转图片工具 - 使用霞鹜文楷字体渲染 markdown 表格为图片
用于百家号发布（编辑器表格渲染效果差）

用法：
    python table_to_image.py <input.md> --slug <slug-name>

示例：
    python table_to_image.py bjh-21.md --slug ai-cutout-tools-compare
"""

import re
import sys
import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("错误：需要 Pillow 库", file=sys.stderr)
    sys.exit(1)


# 霞鹜文楷字体路径（站点已托管）
LXGW_FONT_PATH = Path(__file__).parent.parent / "assets" / "fonts" / "LXGWWenKaiLite-Medium.woff2"


def extract_tables(content):
    """从 markdown 内容中提取所有表格"""
    tables = []
    lines = content.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 检测表格行（以 | 开头）
        if line.startswith('|') and line.endswith('|'):
            table_start = i

            # 读取整个表格
            table_lines = [line]
            i += 1

            # 跳过分隔行 (|---|---|)
            while i < len(lines) and lines[i].strip().startswith('|') and '---' in lines[i]:
                table_lines.append(lines[i])
                i += 1

            # 读取数据行
            while i < len(lines):
                l = lines[i].strip()
                if l.startswith('|') and l.endswith('|'):
                    table_lines.append(l)
                    i += 1
                else:
                    break

            # 解析表格
            if len(table_lines) >= 3:  # 至少表头+分隔+一行数据
                try:
                    table_data = parse_table(table_lines)
                    if table_data:
                        tables.append({
                            'start_line': table_start,
                            'lines': table_lines,
                            'data': table_data,
                            'row_count': len(table_data['rows']) + 1,  # +1 for header
                            'col_count': len(table_data['headers'])
                        })
                except Exception as e:
                    print(f"警告：解析表格失败 (line {i}): {e}", file=sys.stderr)

        i += 1

    return tables


def parse_table(table_lines):
    """解析表格行，返回结构化数据"""
    # 移除首尾的 |
    clean_lines = [l.strip()[1:-1] for l in table_lines if l.strip()]

    # 跳过分隔行
    clean_lines = [l for l in clean_lines if '---' not in l]

    if not clean_lines:
        return None

    # 解析每行的单元格
    rows = []
    for line in clean_lines:
        # 按 | 分割，处理转义字符
        cells = [cell.strip() for cell in line.split('|')]
        # 移除可能的空字符串
        cells = [c for c in cells if c]
        rows.append(cells)

    if not rows:
        return None

    headers = rows[0]
    data_rows = rows[1:]

    return {
        'headers': headers,
        'rows': data_rows
    }


def get_font(size):
    """加载霞鹜文楷字体"""
    try:
        return ImageFont.truetype(str(LXGW_FONT_PATH), size)
    except:
        # 回退到微软雅黑
        fallback_paths = [
            r"C:\Windows\Fonts\msyh.ttc",
            r"C:\Windows\Fonts\simhei.ttf",
        ]
        for path in fallback_paths:
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
        return ImageFont.load_default()


def render_table_to_image(table_data, output_path, max_width=1920):
    """将表格渲染为图片（霞鹜文楷 + 1080P + 零 padding）"""
    headers = table_data['headers']
    rows = table_data['rows']

    # 目标尺寸（1080P）
    target_width = max_width  # 默认 1920
    target_height = 1080

    # 字体大小（大字体确保清晰可读）
    header_font_size = 52
    cell_font_size = 48

    header_font = get_font(header_font_size)
    cell_font = get_font(cell_font_size)

    # 计算列宽（根据内容自适应）
    col_widths = []
    for i, h in enumerate(headers):
        max_len = len(h)
        for row in rows:
            if i < len(row):
                max_len = max(max_len, len(row[i]))
        # 每个字符约 26px（52px 字体），最小宽度确保可读性
        col_widths.append(max(max_len * 26 + 40, 180))

    total_width = sum(col_widths)

    # 如果总宽度小于目标宽度，按比例放大列宽
    if total_width < target_width:
        scale = target_width / total_width
        col_widths = [int(w * scale) for w in col_widths]
        total_width = sum(col_widths)
    # 如果超过目标宽度，缩小
    elif total_width > target_width:
        scale = target_width / total_width
        col_widths = [int(w * scale) for w in col_widths]
        total_width = sum(col_widths)

    # 计算行高（适应大字体）
    row_height = int(cell_font_size * 2.8)  # 约 134px
    header_height = int(header_font_size * 2.8)  # 约 146px

    # 计算总高度（内容高度）
    content_height = header_height + len(rows) * row_height

    # 如果内容高度小于目标高度，按比例放大行高来填充
    if content_height < target_height:
        scale_height = target_height / content_height
        row_height = int(row_height * scale_height)
        header_height = int(header_height * scale_height)
        content_height = header_height + len(rows) * row_height

    # 最终尺寸（四舍五入到偶数，避免 JPEG 压缩问题）
    total_width = total_width // 2 * 2
    total_height = content_height // 2 * 2

    # 创建图片（白色背景）
    img = Image.new('RGB', (total_width, total_height), color='white')
    draw = ImageDraw.Draw(img)

    # 颜色定义（简洁线框风格）
    line_color = '#d1d5db'   # 浅灰分隔线
    header_color = '#f5f5f5'  # 表头浅灰背景
    text_color = '#333333'   # 深灰文字
    header_text_color = '#333333'  # 表头文字

    # 绘制表头（浅灰背景）
    x = 0  # 零 padding
    for i, h in enumerate(headers):
        cell_width = col_widths[i]
        # 表头背景
        draw.rectangle([x, 0, x + cell_width, header_height],
                       fill=header_color)
        # 表头文字
        draw.text((x + cell_width // 2, header_height // 2), h,
                  fill=header_text_color, font=header_font, anchor='mm')
        x += cell_width

    # 绘制数据行（只有底线分隔）
    y = header_height
    for row_idx, row in enumerate(rows):
        x = 0  # 零 padding
        for i, cell in enumerate(row):
            cell_width = col_widths[i]
            # 绘制底线（分隔线）
            draw.line([(0, y), (total_width, y)], fill=line_color, width=1)
            # 绘制单元格文字
            draw.text((x + cell_width // 2, y + row_height // 2), cell,
                      fill=text_color, font=cell_font, anchor='mm')
            x += cell_width
        y += row_height

    # 绘制最后一行底线
    draw.line([(0, y), (total_width, y)], fill=line_color, width=1)

    # 保存为 JPEG（高质量）
    img.save(output_path, 'JPEG', quality=95)
    return True


def process_file(input_file, slug, output_dir=None, max_width=800):
    """处理单个文件，提取表格并生成图片"""
    # 读取内容
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取表格
    tables = extract_tables(content)

    if not tables:
        print(f"未检测到表格: {input_file}", file=sys.stderr)
        return []

    print(f"找到 {len(tables)} 个表格")

    # 确定输出目录（默认 publish-queue-covers，与发布脚本约定一致）
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "publish-queue-covers"
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 处理每个表格
    images = []
    for i, table_info in enumerate(tables):
        table_num = i + 1
        # 命名规范：<slug>-table-N.jpg（避免多文章冲突）
        output_path = output_dir / f"{slug}-table-{table_num}.jpg"

        try:
            render_table_to_image(table_info['data'], str(output_path), max_width)
            print(f"✓ 表格 {table_num} 已保存: {output_path}")
            images.append({
                'path': str(output_path),
                'relative_path': f"../publish-queue-covers/{slug}-table-{table_num}.jpg"
            })
        except Exception as e:
            print(f"✗ 表格 {table_num} 渲染失败: {e}", file=sys.stderr)

    return images


def main():
    if len(sys.argv) < 2:
        print("用法: python table_to_image.py <input.md> --slug <slug-name>")
        print("示例:")
        print("  python table_to_image.py bjh-21.md --slug ai-cutout-tools-compare")
        sys.exit(1)

    input_file = sys.argv[1]

    # 解析参数
    slug = None
    output_dir = None
    max_width = 1920  # 默认 1080P 宽度
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--slug' and i + 1 < len(sys.argv):
            slug = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--width' and i + 1 < len(sys.argv):
            max_width = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    if not slug:
        print("错误：必须指定 --slug 参数", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(input_file):
        print(f"错误：文件不存在: {input_file}", file=sys.stderr)
        sys.exit(1)

    images = process_file(input_file, slug, output_dir, max_width)

    if images:
        print(f"\n生成 {len(images)} 张表格图片")
        print("\n引用格式：")
        for img in images:
            print(f"  ![{img['path'].split('/')[-1].replace('.jpg', '')}](../assets/figures/{slug}/tables/{img['path'].split('/')[-1]})")
    else:
        print("没有生成任何图片")
        sys.exit(1)


if __name__ == '__main__':
    main()
