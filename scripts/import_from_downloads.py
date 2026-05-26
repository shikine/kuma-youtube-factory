"""
Downloadsフォルダから最新4枚の画像をepisodeのinboxにコピーし、
scene1.png〜scene4.pngに整理する。

使い方:
    py scripts/import_from_downloads.py "11_ツバメ"

オプション:
    --n 4        何枚取得するか（デフォルト4）
    --move       コピーではなく移動する
    --yes        確認をスキップする
"""

import argparse
import shutil
import sys
from pathlib import Path

from paths import get_paths
from prepare_manual_images import backup_existing_scene_images, convert_to_png

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
DOWNLOADS_DIR = Path.home() / "Downloads"


def find_recent_images(downloads_dir: Path, n: int) -> list[Path]:
    files = [
        f for f in downloads_dir.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTS
    ]
    files.sort(key=lambda f: f.stat().st_mtime)
    return files[-n:]


def confirm(files: list[Path]) -> bool:
    print("\n以下の画像を使います（古い順 = scene1〜）:\n")
    for i, f in enumerate(files, 1):
        print(f"  scene{i}.png ← {f.name}")
    print()
    ans = input("続けますか？ [y/N]: ").strip().lower()
    return ans == "y"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4, help="取得枚数")
    parser.add_argument("--move", action="store_true", help="コピーでなく移動")
    parser.add_argument("--yes", action="store_true", help="確認をスキップ")
    args = parser.parse_args()

    paths = get_paths()
    image_dir: Path = paths["IMAGE_DIR"]
    image_dir.mkdir(parents=True, exist_ok=True)

    if not DOWNLOADS_DIR.exists():
        print(f"Downloadsフォルダが見つかりません: {DOWNLOADS_DIR}")
        sys.exit(1)

    files = find_recent_images(DOWNLOADS_DIR, args.n)

    if len(files) < args.n:
        print(f"画像が足りません。Downloads内の対象ファイル: {len(files)}枚 / 必要: {args.n}枚")
        sys.exit(1)

    if not args.yes and not confirm(files):
        print("キャンセルしました。")
        sys.exit(0)

    backup_existing_scene_images()

    for i, src in enumerate(files, 1):
        dst = image_dir / f"scene{i}.png"
        print(f"{src.name}  →  scene{i}.png")
        convert_to_png(src, dst)
        if args.move:
            src.unlink()

    print(f"\n完了: {image_dir}")


if __name__ == "__main__":
    main()
