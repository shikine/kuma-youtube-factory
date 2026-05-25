import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

ROOT_DIR = Path(__file__).resolve().parents[1]
CLIENT_SECRET_FILE = ROOT_DIR / "client_secret.json"
TOKEN_FILE = ROOT_DIR / "token.json"
ANALYTICS_RAW_DIR = ROOT_DIR / "analytics" / "raw"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.upload",
]


def get_authenticated_service():
    creds = None

    if TOKEN_FILE.exists():
        # creds.scopes は from_authorized_user_file に渡した SCOPES を返すため、
        # 実際に付与されているスコープは JSON から直接読む
        token_data = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
        granted = set(token_data.get("scopes", []))
        required = set(SCOPES)

        if required.issubset(granted):
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        else:
            print("token.json のスコープが不足しています。再認証が必要です。")
            print("ブラウザが開きます。Googleアカウントで認証してください。")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
        print(f"token.json を更新しました: {TOKEN_FILE}")

    return build("youtube", "v3", credentials=creds)


def get_channel_info(youtube):
    response = youtube.channels().list(
        part="snippet,contentDetails",
        mine=True
    ).execute()

    if not response.get("items"):
        raise RuntimeError("チャンネルが見つかりませんでした。")

    item = response["items"][0]
    channel_id = item["id"]
    uploads_playlist_id = item["contentDetails"]["relatedPlaylists"]["uploads"]
    return channel_id, uploads_playlist_id


def get_video_ids(youtube, playlist_id, max_results):
    video_ids = []
    page_token = None

    while len(video_ids) < max_results:
        fetch_count = min(50, max_results - len(video_ids))
        response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=fetch_count,
            pageToken=page_token
        ).execute()

        for item in response.get("items", []):
            video_ids.append(item["contentDetails"]["videoId"])

        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return video_ids


def get_video_stats(youtube, video_ids):
    videos = []

    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        response = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(batch)
        ).execute()

        for item in response.get("items", []):
            snippet = item["snippet"]
            stats = item.get("statistics", {})
            video_id = item["id"]

            videos.append({
                "video_id": video_id,
                "title": snippet.get("title", ""),
                "published_at": snippet.get("publishedAt", ""),
                "view_count": int(stats.get("viewCount", 0)),
                "like_count": int(stats.get("likeCount", 0)),
                "comment_count": int(stats.get("commentCount", 0)),
                "video_url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail_url": (
                    snippet.get("thumbnails", {})
                    .get("high", {})
                    .get("url", "")
                ),
                "description": snippet.get("description", ""),
                "tags": snippet.get("tags", []),
            })

    return videos


def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def save_csv(videos, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "video_id", "title", "published_at",
        "view_count", "like_count", "comment_count",
        "video_url", "thumbnail_url", "description", "tags",
    ]
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for v in videos:
            row = dict(v)
            row["tags"] = "|".join(v.get("tags") or [])
            writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(
        description="YouTubeチャンネルの動画統計を取得します"
    )
    parser.add_argument(
        "--max-results", type=int, default=50,
        help="取得する動画の最大件数（デフォルト: 50）"
    )
    args = parser.parse_args()

    if not CLIENT_SECRET_FILE.exists():
        print(f"client_secret.json がありません: {CLIENT_SECRET_FILE}")
        sys.exit(1)

    print("YouTube認証中...")
    youtube = get_authenticated_service()

    print("チャンネル情報を取得中...")
    channel_id, playlist_id = get_channel_info(youtube)
    print(f"channel_id: {channel_id}")

    print(f"動画IDを取得中（最大 {args.max_results} 件）...")
    video_ids = get_video_ids(youtube, playlist_id, args.max_results)
    print(f"動画ID取得: {len(video_ids)} 件")

    print("動画統計を取得中...")
    videos = get_video_stats(youtube, video_ids)
    videos.sort(key=lambda v: v["published_at"], reverse=True)

    result = {
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "channel_id": channel_id,
        "videos": videos,
    }

    json_path = ANALYTICS_RAW_DIR / "youtube_video_stats.json"
    csv_path = ANALYTICS_RAW_DIR / "youtube_video_stats.csv"

    save_json(result, json_path)
    save_csv(videos, csv_path)

    print(f"JSON保存: {json_path}")
    print(f"CSV保存: {csv_path}")
    print(f"取得完了: {len(videos)} 件")


if __name__ == "__main__":
    main()
