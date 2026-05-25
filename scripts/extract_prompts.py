import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_JSON = BASE_DIR / "input" / "episode.json"
PROMPT_DIR = BASE_DIR / "assets" / "prompts"

PROMPT_DIR.mkdir(parents=True, exist_ok=True)

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

scenes = data.get("scenes", [])

if not scenes:
    raise ValueError("episode.json に scenes が見つかりません")

for i, scene in enumerate(scenes, start=1):
    prompt = scene.get("image_prompt", "")
    if not prompt:
        print(f"scene{i}: image_prompt が空です")
        continue

    output_path = PROMPT_DIR / f"scene{i}_prompt.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    print(f"作成しました: {output_path}")

print("画像プロンプトの抽出が完了しました。")