import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

def get_episode_dir():

    if len(sys.argv) < 2:
        raise RuntimeError(
            '動画フォルダを指定してください。例: py scripts\\run_all.py "01_ダンゴムシ"'
        )

    arg = Path(sys.argv[1])

    if arg.is_absolute():
        episode_dir = arg

    else:

        candidate1 = ROOT_DIR / arg
        candidate2 = ROOT_DIR / "episodes" / arg

        if candidate1.exists():
            episode_dir = candidate1
        else:
            episode_dir = candidate2

    if not episode_dir.exists():
        raise FileNotFoundError(
            f"動画フォルダが見つかりません: {episode_dir}"
        )

    return episode_dir

def get_paths():

    episode_dir = get_episode_dir()

    return {

        "ROOT_DIR": ROOT_DIR,

        "EPISODE_DIR": episode_dir,

        "INPUT_JSON":
            episode_dir / "input" / "episode.json",

        "IMAGE_DIR":
            episode_dir / "assets" / "images",

        "VOICE_DIR":
            episode_dir / "assets" / "voices",

        "BGM_FILE":
            episode_dir / "assets" / "bgm" / "main_bgm.mp3",

        "SHARED_BGM_FILE":
            ROOT_DIR / "shared" / "bgm" / "main_bgm.mp3",

        "OUTPUT_DIR":
            episode_dir / "output",

        "TEMP_DIR":
            episode_dir / "output" / "temp",

        "FINAL_VIDEO":
            episode_dir / "output" / "final.mp4",
    }