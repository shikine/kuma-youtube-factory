import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

if len(sys.argv) < 2:
    raise RuntimeError(
        '動画フォルダを指定してください。例: py scripts\\run_after_images.py "04_ホタル"'
    )

episode_arg = sys.argv[1]

steps = [
    ("BGM自動取得",    "download_bgm.py"),
    ("手動格納画像の整理", "prepare_manual_images.py"),
    ("VOICEVOX音声生成", "generate_voice.py"),
    ("動画生成+BGM",   "make_video.py"),
]

for label, script in steps:
    print(f"\n=== {label} 開始 ===")

    subprocess.run(
        [
            "py",
            str(ROOT_DIR / "scripts" / script),
            episode_arg
        ],
        check=True
    )

    print(f"=== {label} 完了 ===")

print("\nすべて完了しました。")
print("YouTubeアップロードは以下で実行してください:")
print(f'  py scripts\\upload_youtube.py "{episode_arg}"')