import json
import sys
from pathlib import Path

from googleapiclient.http import MediaFileUpload

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import get_paths
from drive_service import get_drive_service

ROOT_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT_DIR / ".env"


def load_env():
    if not ENV_FILE.exists():
        return {}
    env = {}
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    return env


def get_or_create_folder(service, name, parent_id=None):
    q = (
        f"name='{name}' and mimeType='application/vnd.google-apps.folder'"
        " and trashed=false"
    )
    if parent_id:
        q += f" and '{parent_id}' in parents"
    results = service.files().list(q=q, fields="files(id)").execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]
    metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent_id:
        metadata["parents"] = [parent_id]
    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]


def upload_file(service, local_path, folder_id):
    if not local_path.exists():
        print(f"  スキップ（未生成）: {local_path.name}")
        return
    name = local_path.name
    q = f"name='{name}' and '{folder_id}' in parents and trashed=false"
    existing = service.files().list(q=q, fields="files(id)").execute().get("files", [])
    media = MediaFileUpload(str(local_path), resumable=True)
    if existing:
        service.files().update(fileId=existing[0]["id"], media_body=media).execute()
        print(f"  更新: {name}")
    else:
        metadata = {"name": name, "parents": [folder_id]}
        service.files().create(body=metadata, media_body=media, fields="id").execute()
        print(f"  アップロード: {name}")


def main():
    paths = get_paths()
    episode_dir = paths["EPISODE_DIR"]
    episode_name = episode_dir.name
    input_json = paths["INPUT_JSON"]

    episode_data = json.loads(input_json.read_text(encoding="utf-8"))

    env = load_env()
    parent_id = env.get("DRIVE_ROOT_FOLDER_ID", "").strip() or None

    service = get_drive_service()

    folder_id = episode_data.get("drive_folder_id", "").strip()
    if not folder_id:
        print(f"Driveフォルダを作成: {episode_name}")
        folder_id = get_or_create_folder(service, episode_name, parent_id)
        episode_data["drive_folder_id"] = folder_id
        input_json.write_text(
            json.dumps(episode_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"  drive_folder_id を episode.json に保存しました")
    else:
        print(f"Driveフォルダ使用: {folder_id}")

    print("\n--- episode.json ---")
    upload_file(service, input_json, folder_id)

    print("\n--- 画像 ---")
    for i in range(1, 5):
        upload_file(service, paths["IMAGE_DIR"] / f"scene{i}.png", folder_id)

    print("\n--- 音声 ---")
    for i in range(1, 5):
        upload_file(service, paths["VOICE_DIR"] / f"scene{i}.wav", folder_id)

    print("\n--- BGM ---")
    upload_file(service, paths["BGM_FILE"], folder_id)

    print("\n--- 動画 ---")
    upload_file(service, paths["FINAL_VIDEO"], folder_id)

    print(f"\nDriveアップロード完了！")
    print(f"フォルダURL: https://drive.google.com/drive/folders/{folder_id}")


if __name__ == "__main__":
    main()
