import shutil
import subprocess

from paths import get_paths

paths = get_paths()

IMAGE_DIR = paths["IMAGE_DIR"]
VOICE_DIR = paths["VOICE_DIR"]

BGM_FILE = paths["BGM_FILE"]
SHARED_BGM_FILE = paths["SHARED_BGM_FILE"]

TEMP_DIR = paths["TEMP_DIR"]
OUTPUT = paths["FINAL_VIDEO"]

TEMP_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# 共通BGMコピー
if not BGM_FILE.exists() and SHARED_BGM_FILE.exists():

    BGM_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    shutil.copy(
        SHARED_BGM_FILE,
        BGM_FILE
    )

scene_files = []

for i in range(1, 5):

    image = IMAGE_DIR / f"scene{i}.png"
    voice = VOICE_DIR / f"scene{i}.wav"

    scene_video = TEMP_DIR / f"scene{i}.mp4"

    if not image.exists():
        raise FileNotFoundError(
            f"画像がありません: {image}"
        )

    if not voice.exists():
        raise FileNotFoundError(
            f"音声がありません: {voice}"
        )

    cmd = [
        "ffmpeg",
        "-y",

        "-loop", "1",
        "-i", str(image),

        "-i", str(voice),

        "-vf",
        "scale=1080:1920:"
        "force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        "format=yuv420p",

        "-c:v", "libx264",
        "-tune", "stillimage",

        "-c:a", "aac",
        "-b:a", "192k",

        "-shortest",

        str(scene_video)
    ]

    subprocess.run(
        cmd,
        check=True
    )

    scene_files.append(scene_video)

concat_file = TEMP_DIR / "concat.txt"

with open(
    concat_file,
    "w",
    encoding="utf-8"
) as f:

    for file in scene_files:
        f.write(
            f"file '{file.as_posix()}'\n"
        )

merged_video = TEMP_DIR / "merged.mp4"

cmd_concat = [
    "ffmpeg",
    "-y",

    "-f", "concat",
    "-safe", "0",

    "-i", str(concat_file),

    "-c", "copy",

    str(merged_video)
]

subprocess.run(
    cmd_concat,
    check=True
)

if not BGM_FILE.exists():
    raise FileNotFoundError(
        f"BGMがありません: {BGM_FILE}"
    )

cmd_bgm = [
    "ffmpeg",
    "-y",

    "-i", str(merged_video),

    "-stream_loop", "-1",
    "-i", str(BGM_FILE),

    "-filter_complex",
    "[1:a]volume=0.08[bgm];"
    "[0:a][bgm]amix=inputs=2:duration=first",

    "-c:v", "copy",

    "-c:a", "aac",
    "-b:a", "192k",

    str(OUTPUT)
]

subprocess.run(
    cmd_bgm,
    check=True
)

print(f"完成しました: {OUTPUT}")