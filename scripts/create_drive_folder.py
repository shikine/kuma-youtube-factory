"""
Googleドライブに episode フォルダを作成し、drive_folder_id を episode.json に書き込む。

初回のみブラウザ認証が必要。以降は drive_rw_token.json のリフレッシュトークンで
スマホや remote 環境からでも自動実行できる。

前提:
  - client_secret.json をプロジェクトルートに配置済み
  - .env に DRIVE_PARENT_FOLDER_ID=<親フォルダのID> を設定済み

使い方:
  py scripts/create_drive_folder.py "11_ルバーブ"
"""

import json
import sys
from pathlib import Path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import get_paths

# Drive ファイル作成・フォルダ管理に必要な最小スコープ
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

ROOT_DIR = Path(__file__).resolve().parents[1]
CLIENT_SECRET_FILE = ROOT_DIR / "client_secret.json"
TOKEN_FILE = ROOT_DIR / "drive_rw_token.json"
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


def get_drive_service():
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET_FILE.exists():
                raise FileNotFoundError(
                    f"client_secret.json がありません: {CLIENT_SECRET_FILE}\n"
                    "Google Cloud Console からダウンロードして配置してください。"
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
        print(f"認証トークンを保存しました: {TOKEN_FILE}")

    return build("drive", "v3", credentials=creds)


def create_folder(service, folder_name, parent_folder_id=None):
    metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_folder_id:
        metadata["parents"] = [parent_folder_id]

    folder = service.files().create(
        body=metadata,
        fields="id, name, webViewLink"
    ).execute()

    return folder


def update_drive_folder_id(episode_json_path, folder_id):
    data = json.loads(episode_json_path.read_text(encoding="utf-8"))
    data["drive_folder_id"] = folder_id
    episode_json_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def main():
    paths = get_paths()
    episode_json = paths["INPUT_JSON"]
    episode_data = json.loads(episode_json.read_text(encoding="utf-8"))

    folder_name = episode_data.get("folder_name", "")
    if not folder_name:
        raise RuntimeError("episode.json に folder_name がありません。")

    existing_id = episode_data.get("drive_folder_id", "").strip()
    if existing_id:
        print(f"drive_folder_id は既に設定済みです: {existing_id}")
        print("再作成する場合は episode.json の drive_folder_id を空にしてから実行してください。")
        return

    env = load_env()
    parent_folder_id = env.get("DRIVE_PARENT_FOLDER_ID", "").strip() or None

    if not parent_folder_id:
        print("警告: .env に DRIVE_PARENT_FOLDER_ID が未設定のため、マイドライブ直下に作成します。")

    print(f"Googleドライブにフォルダを作成中: {folder_name}")
    service = get_drive_service()
    folder = create_folder(service, folder_name, parent_folder_id)

    folder_id = folder["id"]
    web_link = folder.get("webViewLink", "")

    update_drive_folder_id(episode_json, folder_id)

    print(f"フォルダ作成完了!")
    print(f"  フォルダ名  : {folder['name']}")
    print(f"  folder_id   : {folder_id}")
    print(f"  Drive URL   : {web_link}")
    print(f"  episode.json: drive_folder_id を更新しました")


if __name__ == "__main__":
    main()
