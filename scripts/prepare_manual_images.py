import shutil
from pathlib import Path

from PIL import Image

from paths import get_paths

paths = get_paths()

IMAGE_DIR = paths["IMAGE_DIR"]
INBOX_DIR = IMAGE_DIR / "inbox"

IMAGE_EXTS = [".png", ".jpg", ".jpeg", ".webp"]

IMAGE_DIR.mkdir(parents=True, exist_ok=True)
INBOX_DIR.mkdir(parents=True, exist_ok=True)

def collect_images():
    files = []

    for file in INBOX_DIR.iterdir():
        if file.is_file() and file.suffix.lower() in IMAGE_EXTS:
            files.append(file)

    # 更新日時が古い順。01.png, 02.png などにしておくと順番管理しやすい
    files.sort(key=lambda p: p.stat().st_mtime)

    return files

def backup_existing_scene_images():
    backup_dir = IMAGE_DIR / "backup"
    backup_dir.mkdir(exist_ok=True)

    for i in range(1, 5):
        scene_path = IMAGE_DIR / f"scene{i}.png"

        if scene_path.exists():
            backup_path = backup_dir / f"scene{i}.png"
            shutil.copy(scene_path, backup_path)
            scene_path.unlink()

def convert_to_png(src, dst):
    with Image.open(src) as img:
        img = img.convert("RGB")
        img.save(dst, "PNG")

def delete_inbox():
    if INBOX_DIR.exists():
        shutil.rmtree(INBOX_DIR)
        print(f"inbox を削除しました: {INBOX_DIR}")

def main():
    files = collect_images()

    if len(files) < 4:
        raise RuntimeError(
            f"inbox に画像が4枚必要です。現在 {len(files)} 枚です: {INBOX_DIR}"
        )

    if len(files) > 4:
        print(f"画像が {len(files)} 枚あります。更新日時が古い順に4枚だけ使います。")

    selected = files[:4]

    backup_existing_scene_images()

    for i, src in enumerate(selected, start=1):
        dst = IMAGE_DIR / f"scene{i}.png"

        print(f"{src.name} -> scene{i}.png")

        convert_to_png(src, dst)

    delete_inbox()

    print("画像整理完了")
    print(f"保存先: {IMAGE_DIR}")

if __name__ == "__main__":
    main()