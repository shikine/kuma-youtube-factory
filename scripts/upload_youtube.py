import json
import os

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from paths import get_paths

paths = get_paths()

ROOT_DIR = paths["ROOT_DIR"]
EPISODE_JSON = paths["INPUT_JSON"]
VIDEO_FILE = paths["FINAL_VIDEO"]

CLIENT_SECRET_FILE = ROOT_DIR / "client_secret.json"
TOKEN_FILE = ROOT_DIR / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]

def get_authenticated_service():

    creds = None
    from_env = False

    token_json = os.environ.get("GOOGLE_YOUTUBE_TOKEN")
    if token_json:
        creds = Credentials.from_authorized_user_info(
            json.loads(token_json),
            SCOPES
        )
        from_env = True
    elif TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(
            str(TOKEN_FILE),
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

            if from_env:
                print("トークンを自動更新しました。環境変数 GOOGLE_YOUTUBE_TOKEN を更新してください:")
                print(creds.to_json())
            else:
                TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

        else:

            if not CLIENT_SECRET_FILE.exists():
                raise FileNotFoundError(
                    "YouTube 認証ができません。以下のいずれかが必要です:\n"
                    "  1. 環境変数 GOOGLE_YOUTUBE_TOKEN にトークンJSONを設定する\n"
                    "     → PCで scripts/setup_tokens.py を実行して取得できます\n"
                    "  2. client_secret.json を配置してブラウザ認証を行う\n"
                    "     → スマホ・クラウド環境では動作しません"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE),
                SCOPES
            )

            creds = flow.run_local_server(port=0)
            TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return build(
        "youtube",
        "v3",
        credentials=creds
    )

def main():

    if not CLIENT_SECRET_FILE.exists():
        raise FileNotFoundError(
            f"client_secret.json がありません: {CLIENT_SECRET_FILE}"
        )

    if not VIDEO_FILE.exists():
        raise FileNotFoundError(
            f"動画がありません: {VIDEO_FILE}"
        )

    data = json.loads(
        EPISODE_JSON.read_text(
            encoding="utf-8"
        )
    )

    title = data.get(
        "title",
        "クマ博士の森のいきもの研究所"
    )

    description = data.get(
        "description",
        ""
    )

    hashtags = data.get(
        "hashtags",
        []
    )

    if isinstance(hashtags, list):
        description += "\n\n" + " ".join(hashtags)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": [
                tag.replace("#", "")
                for tag in hashtags
            ] if isinstance(hashtags, list) else [],
            "categoryId": "27"
        },
        "status": {
            "privacyStatus": "unlisted",
            "selfDeclaredMadeForKids": True
        }
    }

    youtube = get_authenticated_service()

    media = MediaFileUpload(
        str(VIDEO_FILE),
        chunksize=-1,
        resumable=True,
        mimetype="video/mp4"
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    print("YouTubeへアップロード中...")

    response = None

    while response is None:

        status, response = request.next_chunk()

        if status:
            print(
                f"進捗: {int(status.progress() * 100)}%"
            )

    video_id = response["id"]

    print("アップロード完了")
    print(
        f"https://www.youtube.com/watch?v={video_id}"
    )

if __name__ == "__main__":
    main()