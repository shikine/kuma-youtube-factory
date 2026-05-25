import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import get_paths

paths = get_paths()
input_json = paths["INPUT_JSON"]

with open(input_json, "r", encoding="utf-8") as f:
    data = json.load(f)

scenes = data.get("scenes", [])
if not scenes:
    raise ValueError("episode.json に scenes が見つかりません")

print(f"\n{'='*60}")
print(f"  {data.get('title', '')}  画像生成プロンプト")
print(f"{'='*60}\n")

for scene in scenes:
    n = scene["scene"]
    role = scene.get("role", "")
    prompt = scene.get("image_prompt", "")
    print(f"--- Scene {n}：{role} ---")
    print(prompt)
    print()
