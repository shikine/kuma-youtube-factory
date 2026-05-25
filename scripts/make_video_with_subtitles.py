import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_VIDEO = BASE_DIR / "output" / "final.mp4"
SUBTITLE_FILE = BASE_DIR / "output" / "subtitles.srt"
OUTPUT_VIDEO = BASE_DIR / "output" / "final_subtitled.mp4"

subtitle_path = SUBTITLE_FILE.as_posix().replace(":", "\\:")

vf_arg = (
    f"subtitles='{subtitle_path}':"
    "force_style='Fontsize=18,"
    "PrimaryColour=&Hffffff&,"
    "OutlineColour=&H000000&,"
    "BorderStyle=1,"
    "Outline=2,"
    "Shadow=1,"
    "Alignment=2'"
)

cmd = [
    "ffmpeg",
    "-y",
    "-i", str(INPUT_VIDEO),
    "-vf", vf_arg,
    "-c:a", "copy",
    str(OUTPUT_VIDEO)
]

subprocess.run(cmd, check=True)

print(f"字幕入り動画完成: {OUTPUT_VIDEO}")