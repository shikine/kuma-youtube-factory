import random
import shutil
import sys
from datetime import datetime
from pathlib import Path

import requests

from paths import get_paths

paths = get_paths()

BGM_FILE = paths["BGM_FILE"]
SHARED_BGM_FILE = paths["SHARED_BGM_FILE"]
BGM_FILE.parent.mkdir(parents=True, exist_ok=True)

SEARCH_WORDS = [
    "ambient nature",
    "calm ambient",
    "soft forest music",
    "peaceful background music",
    "gentle ambient",
]

OPENVERSE_API = "https://api.openverse.org/v1/audio/"


def search_openverse_audio(query):
    params = {
        "q": query,
        "license_type": "commercial",
        "page_size": 20,
    }
    res = requests.get(OPENVERSE_API, params=params, timeout=30)
    res.raise_for_status()
    return res.json().get("results", [])


def pick_audio(results):
    candidates = []
    for item in results:
        url = item.get("url")
        filetype = item.get("filetype", "")
        if not url:
            continue
        if filetype and filetype.lower() not in ["mp3", "wav", "ogg"]:
            continue
        candidates.append({
            "url": url,
            "title": item.get("title", ""),
            "creator": item.get("creator", ""),
            "license": item.get("license", ""),
            "filetype": filetype,
        })
    return random.choice(candidates) if candidates else None


def download_file(url, output_path):
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


def write_credit(credit_file, **fields):
    lines = [f"{k}: {v}" for k, v in fields.items()]
    credit_file.write_text("\n".join(lines), encoding="utf-8")


def fallback_shared_bgm():
    if not SHARED_BGM_FILE.exists():
        return False
    shutil.copy(SHARED_BGM_FILE, BGM_FILE)
    credit_file = BGM_FILE.parent / "bgm_credit.txt"
    write_credit(
        credit_file,
        source=r"shared\bgm\main_bgm.mp3",
        license="manual / unknown",
        note="共通BGMを使用。必要に応じてライセンスを確認してください。",
    )
    print(f"共通BGMをコピーしました: {BGM_FILE}")
    print(f"クレジット保存完了: {credit_file}")
    return True


def main():
    if BGM_FILE.exists():
        print(f"BGMはすでにあります: {BGM_FILE}")
        return

    random.shuffle(SEARCH_WORDS)

    for query in SEARCH_WORDS:
        print(f"BGM検索中: {query}")
        try:
            results = search_openverse_audio(query)
        except Exception as e:
            print(f"検索失敗: {e}")
            continue

        audio = pick_audio(results)
        if not audio:
            print("候補なし、次のキーワードへ")
            continue

        print(f"BGM候補: {audio['title']} / {audio['creator']} / {audio['license']}")

        try:
            download_file(audio["url"], BGM_FILE)
            credit_file = BGM_FILE.parent / "bgm_credit.txt"
            write_credit(
                credit_file,
                title=audio["title"],
                creator=audio["creator"],
                license=audio["license"],
                url=audio["url"],
                downloaded_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            print(f"BGM保存完了: {BGM_FILE}")
            print(f"クレジット保存完了: {credit_file}")
            return
        except Exception as e:
            print(f"ダウンロード失敗: {e}")
            if BGM_FILE.exists():
                BGM_FILE.unlink()
            continue

    print("Openverseからの取得に失敗しました。共通BGMを確認します...")
    if fallback_shared_bgm():
        return

    print("BGMを取得できませんでした。")
    print(f"手動で {BGM_FILE} を配置してください。")
    sys.exit(1)


if __name__ == "__main__":
    main()
