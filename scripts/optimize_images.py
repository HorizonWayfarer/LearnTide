#!/usr/bin/env python3
"""批量将 JPEG 转换为 WebP，保留原图作为 fallback"""
import os
from pathlib import Path
from PIL import Image

ROOT = Path("A:/LearnTide")
COVERS_DIR = ROOT / "assets" / "covers"
FIGURES_DIR = ROOT / "assets" / "figures"


def convert_jpg_to_webp(jpg_path: Path) -> Path | None:
    """转换单张图片为 WebP，返回 WebP 路径或 None"""
    if not jpg_path.exists():
        return None
    webp_path = jpg_path.with_suffix(".webp")

    # 跳过已转换的
    if webp_path.exists() and webp_path.stat().st_size > 1000:
        return webp_path

    try:
        with Image.open(jpg_path) as img:
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            elif img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')

            img.save(webp_path, 'WEBP', quality=85, optimize=True)

            original_size = jpg_path.stat().st_size
            webp_size = webp_path.stat().st_size
            if webp_size > original_size:
                webp_path.unlink(missing_ok=True)
                return None
            print(f"  [OK] {jpg_path.name}: {original_size//1024}KB -> {webp_size//1024}KB ({(1-webp_size/original_size)*100:.0f}%)")
            return webp_path
    except Exception as e:
        print(f"  [FAIL] {jpg_path.name}: {e}")
        webp_path.unlink(missing_ok=True)
        return None


def main():
    print("=== 批量转换图片为 WebP ===\n")

    converted = 0
    skipped = 0
    errors = 0

    print("处理封面图...")
    for jpg in sorted(COVERS_DIR.glob("*.jpg")):
        try:
            if convert_jpg_to_webp(jpg):
                converted += 1
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"  [FAIL] {jpg.name}: {e}")

    print("\n处理正文配图...")
    for slug_dir in sorted(FIGURES_DIR.iterdir()):
        if not slug_dir.is_dir():
            continue
        for jpg in sorted(slug_dir.glob("*.jpg")):
            try:
                if convert_jpg_to_webp(jpg):
                    converted += 1
                else:
                    skipped += 1
            except Exception as e:
                errors += 1
                print(f"  [FAIL] {slug_dir.name}/{jpg.name}: {e}")

    print(f"\n完成!")
    print(f"  已转换: {converted} 张")
    print(f"  跳过/失败: {skipped + errors} 张")

    original_total = sum(f.stat().st_size for f in COVERS_DIR.glob("*.jpg"))
    original_total += sum(
        f.stat().st_size
        for d in FIGURES_DIR.iterdir()
        if d.is_dir()
        for f in d.glob("*.jpg")
    )
    webp_total = sum(f.stat().st_size for f in COVERS_DIR.glob("*.webp"))
    webp_total += sum(
        f.stat().st_size
        for d in FIGURES_DIR.iterdir()
        if d.is_dir()
        for f in d.glob("*.webp")
    )
    savings = (original_total - webp_total) // 1024 // 1024
    print(f"  节省空间: 约 {savings} MB")


if __name__ == "__main__":
    main()