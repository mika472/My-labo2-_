#!/usr/bin/env python3
"""
カルーセル納品準備スクリプト

使用方法:
  python3 scripts/prepare_carousel_delivery.py <入力ディレクトリ> <出力ディレクトリ> \
    --expected-count 10 --prefix carousel
"""

import argparse
import os
import sys
import zipfile
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="カルーセルページを1080×1350に正規化して納品パッケージを作成する")
    parser.add_argument("input_dir", help="入力画像のディレクトリ")
    parser.add_argument("output_dir", help="出力ディレクトリ")
    parser.add_argument("--expected-count", type=int, required=True, help="期待するページ数")
    parser.add_argument("--prefix", default="carousel", help="出力ファイル名のプレフィックス（デフォルト: carousel）")
    parser.add_argument("--width", type=int, default=1080, help="出力幅（デフォルト: 1080）")
    parser.add_argument("--height", type=int, default=1350, help="出力高さ（デフォルト: 1350）")
    return parser.parse_args()


def find_image_files(input_dir: Path) -> list[Path]:
    extensions = {".png", ".jpg", ".jpeg", ".webp"}
    files = sorted(
        f for f in input_dir.iterdir()
        if f.is_file() and f.suffix.lower() in extensions
    )
    return files


def normalize_image(src: Path, dst: Path, width: int, height: int) -> bool:
    try:
        from PIL import Image
        with Image.open(src) as img:
            img.verify()

        with Image.open(src) as img:
            orig_w, orig_h = img.size
            target_ratio = width / height
            orig_ratio = orig_w / orig_h

            if orig_ratio > target_ratio:
                new_w = int(orig_h * target_ratio)
                left = (orig_w - new_w) // 2
                img = img.crop((left, 0, left + new_w, orig_h))
            elif orig_ratio < target_ratio:
                new_h = int(orig_w / target_ratio)
                top = (orig_h - new_h) // 2
                img = img.crop((0, top, orig_w, top + new_h))

            img = img.resize((width, height), Image.LANCZOS)
            img.save(dst, format="PNG", optimize=True)
        return True
    except Exception as e:
        print(f"  [ERROR] {src.name}: {e}", file=sys.stderr)
        return False


def verify_image(path: Path) -> bool:
    try:
        from PIL import Image
        with Image.open(path) as img:
            img.load()
        return True
    except Exception as e:
        print(f"  [ERROR] 検証失敗 {path.name}: {e}", file=sys.stderr)
        return False


def create_contact_sheet(image_paths: list[Path], output_path: Path, cols: int = 3) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont
        thumb_w, thumb_h = 360, 450
        rows = (len(image_paths) + cols - 1) // cols
        sheet_w = cols * thumb_w
        sheet_h = rows * thumb_h

        sheet = Image.new("RGB", (sheet_w, sheet_h), color=(30, 30, 30))
        draw = ImageDraw.Draw(sheet)

        for i, img_path in enumerate(image_paths):
            row, col = divmod(i, cols)
            x, y = col * thumb_w, row * thumb_h
            with Image.open(img_path) as img:
                thumb = img.resize((thumb_w, thumb_h), Image.LANCZOS)
                sheet.paste(thumb, (x, y))
            draw.text((x + 8, y + 8), img_path.stem, fill=(255, 255, 100))

        sheet.save(output_path, format="PNG")
        return True
    except Exception as e:
        print(f"  [WARN] コンタクトシート作成失敗: {e}", file=sys.stderr)
        return False


def create_zip(image_paths: list[Path], zip_path: Path) -> bool:
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in image_paths:
                zf.write(p, p.name)
        with zipfile.ZipFile(zip_path) as zf:
            result = zf.testzip()
            if result is not None:
                print(f"  [ERROR] ZIPが破損しています: {result}", file=sys.stderr)
                return False
        return True
    except Exception as e:
        print(f"  [ERROR] ZIP作成失敗: {e}", file=sys.stderr)
        return False


def main():
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("[ERROR] Pillowがインストールされていません。pip install Pillow を実行してください。", file=sys.stderr)
        sys.exit(1)

    print(f"\n=== カルーセル納品準備スクリプト ===")
    print(f"入力: {input_dir}")
    print(f"出力: {output_dir}")
    print(f"期待ページ数: {args.expected_count}")
    print(f"出力サイズ: {args.width}×{args.height}")

    source_files = find_image_files(input_dir)
    print(f"\n[1] 入力ファイル: {len(source_files)} 件検出")

    if len(source_files) != args.expected_count:
        print(f"  [WARN] 期待値({args.expected_count})と一致しません。処理を続けます。")

    normalized = []
    print(f"\n[2] 正規化 ({args.width}×{args.height})...")
    for i, src in enumerate(source_files, start=1):
        dst_name = f"{args.prefix}_{i:02d}.png"
        dst = output_dir / dst_name
        ok = normalize_image(src, dst, args.width, args.height)
        if ok:
            print(f"  ✓ {dst_name}")
            normalized.append(dst)
        else:
            print(f"  ✗ {src.name} → スキップ")

    print(f"\n[3] 検証...")
    verified = []
    for p in normalized:
        if verify_image(p):
            print(f"  ✓ {p.name}")
            verified.append(p)
        else:
            print(f"  ✗ {p.name} → 検証失敗")

    contact_path = output_dir / f"{args.prefix}_contact_sheet.png"
    print(f"\n[4] コンタクトシート作成: {contact_path.name}")
    create_contact_sheet(verified, contact_path)

    zip_path = output_dir / f"{args.prefix}_delivery.zip"
    print(f"\n[5] ZIPパッケージ作成: {zip_path.name}")
    zip_ok = create_zip(verified, zip_path)

    print(f"\n=== 完了 ===")
    print(f"正規化成功: {len(normalized)}/{len(source_files)} ページ")
    print(f"検証成功:   {len(verified)}/{len(normalized)} ページ")
    print(f"ZIP:        {'✓ 有効' if zip_ok else '✗ 無効'}")
    print(f"出力先:     {output_dir.resolve()}")

    if len(verified) != args.expected_count or not zip_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
