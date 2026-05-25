import json
import wave
import textwrap
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_JSON = BASE_DIR / "input" / "episode.json"
VOICE_DIR = BASE_DIR / "assets" / "voices"
OUTPUT_SRT = BASE_DIR / "output" / "subtitles.srt"

MAX_CHARS_PER_LINE = 14
MAX_LINES = 2

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def make_two_line_text(text):
    text = text.replace("\n", " ").strip()

    lines = textwrap.wrap(
        text,
        width=MAX_CHARS_PER_LINE,
        break_long_words=False,
        break_on_hyphens=False
    )

    if len(lines) <= MAX_LINES:
        return "\n".join(lines)

    first = lines[0]
    second = "".join(lines[1:])
    second = second[:MAX_CHARS_PER_LINE * 2]

    return first + "\n" + second

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

scenes = data.get("scenes", [])
current_time = 0.0
srt_lines = []

for i, scene in enumerate(scenes, start=1):
    voice_path = VOICE_DIR / f"scene{i}.wav"

    if not voice_path.exists():
        continue

    with wave.open(str(voice_path), "rb") as wav:
        duration = wav.getnframes() / float(wav.getframerate())

    dialogue = scene.get("dialogue", "")
    narration = scene.get("narration", "")

    text = " ".join([t for t in [dialogue, narration] if t])
    subtitle_text = make_two_line_text(text)

    start = current_time
    end = current_time + duration

    srt_lines.append(str(i))
    srt_lines.append(f"{format_time(start)} --> {format_time(end)}")
    srt_lines.append(subtitle_text)
    srt_lines.append("")

    current_time = end

OUTPUT_SRT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_SRT.write_text("\n".join(srt_lines), encoding="utf-8")

print(f"字幕作成完了: {OUTPUT_SRT}")