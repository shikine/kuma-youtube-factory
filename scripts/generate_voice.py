import json
import requests

from paths import get_paths

paths = get_paths()

INPUT_JSON = paths["INPUT_JSON"]
VOICE_DIR = paths["VOICE_DIR"]

VOICE_DIR.mkdir(parents=True, exist_ok=True)

VOICEVOX_URL = "http://127.0.0.1:50021"

# ずんだもん
SPEAKER_ID = 3


def build_voice_text(scene):
    """
    voice_text がある場合は最優先。
    なければ dialogue + narration を使う。
    """
    voice_text = scene.get("voice_text", "").strip()

    if voice_text:
        return voice_text

    dialogue = scene.get("dialogue", "").strip()
    narration = scene.get("narration", "").strip()

    return "\n".join(
        [text for text in [dialogue, narration] if text]
    ).strip()


with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

scenes = data.get("scenes", [])

if not scenes:
    raise ValueError("scenes が見つかりません")

for i, scene in enumerate(scenes, start=1):

    text = build_voice_text(scene)

    if not text:
        print(f"scene{i}: 読み上げテキストなし")
        continue

    print(f"scene{i} 音声生成中...")
    print(f"読み上げ: {text}")

    query_response = requests.post(
        f"{VOICEVOX_URL}/audio_query",
        params={
            "text": text,
            "speaker": SPEAKER_ID
        }
    )

    query_response.raise_for_status()

    audio_query = query_response.json()

    synthesis_response = requests.post(
        f"{VOICEVOX_URL}/synthesis",
        params={
            "speaker": SPEAKER_ID
        },
        json=audio_query
    )

    synthesis_response.raise_for_status()

    output_path = VOICE_DIR / f"scene{i}.wav"

    with open(output_path, "wb") as f:
        f.write(synthesis_response.content)

    print(f"保存しました: {output_path}")

print("音声生成完了")