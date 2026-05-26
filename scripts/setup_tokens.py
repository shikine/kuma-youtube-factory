"""
PC上で一度だけ実行するセットアップスクリプト。
ブラウザでGoogleアカウントにログインし、トークンを取得します。
取得したトークンをClaude Code Webの環境変数に設定することで、
スマホ・クラウド環境からもGoogle Drive/YouTubeにアクセスできます。

使い方（PC上のターミナルで実行）:
  py scripts/setup_tokens.py
"""

import json
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

ROOT_DIR = Path(__file__).resolve().parents[1]
CLIENT_SECRET_FILE = ROOT_DIR / "client_secret.json"

DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

DRIVE_TOKEN_FILE = ROOT_DIR / "drive_token.json"
YOUTUBE_TOKEN_FILE = ROOT_DIR / "token.json"


def get_token(scopes, token_file, service_name):
    creds = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print(f"\n{service_name} の認証ページをブラウザで開きます...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE), scopes
            )
            creds = flow.run_local_server(port=0)

        token_file.write_text(creds.to_json(), encoding="utf-8")

    return creds.to_json()


def main():
    if not CLIENT_SECRET_FILE.exists():
        raise FileNotFoundError(
            f"client_secret.json がありません: {CLIENT_SECRET_FILE}\n"
            "Google Cloud Console でOAuthクライアントIDを作成してダウンロードしてください。"
        )

    print("=" * 60)
    print("クマ博士YouTube工房 - Google認証セットアップ")
    print("=" * 60)

    drive_token = get_token(DRIVE_SCOPES, DRIVE_TOKEN_FILE, "Google Drive")
    youtube_token = get_token(YOUTUBE_SCOPES, YOUTUBE_TOKEN_FILE, "YouTube")

    print("\n" + "=" * 60)
    print("認証完了！以下の手順でClaude Code Webに環境変数を設定してください")
    print("=" * 60)
    print()
    print("【設定場所】")
    print("  Claude Code Web → 環境設定 → Environment Variables")
    print()
    print("【環境変数名と値】")
    print()
    print("変数名: GOOGLE_DRIVE_TOKEN")
    print("値（以下をそのままコピー）:")
    print(drive_token)
    print()
    print("変数名: GOOGLE_YOUTUBE_TOKEN")
    print("値（以下をそのままコピー）:")
    print(youtube_token)
    print()
    print("=" * 60)
    print("設定後はスマホのClaude Code WebからDrive/YouTubeが使えます。")
    print("=" * 60)


if __name__ == "__main__":
    main()
