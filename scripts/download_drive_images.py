import io
import sys
from pathlib import Path

from googleapiclient.http import MediaIoBaseDownload
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import get_paths
from drive_service import get_drive_service

IMAGE_MIMETYPES = {"image/png", "image/jpeg", "image/webp"}

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


def download_images(service, folder_id, image_dir):
    image_dir.mkdir(parents=True, exist_ok=True)

    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="files(id, name, mimeType)",
        orderBy="name"
    ).execute()

    files = [
        f for f in results.get("files", [])
        if f["mimeType"] in IMAGE_MIMETYPES
    ]

    if len(files) < 4:
        raise RuntimeError(
            f"Drive フォルダに画像が4枚必要です。現在 {len(files)} 枚: "
            f"{[f['name'] for f in files]}"
        )

    if len(files) > 4:
        print(f"画像が {len(files)} 枚あります。名前順で4枚使います。")

    for i, file in enumerate(files[:4], start=1):
        dst = image_dir / f"scene{i}.png"
        print(f"  {file['name']} -> scene{i}.png")

        request = service.files().get_media(fileId=file["id"])
        buf = io.BytesIO()
        downloader = MediaIoBaseDownload(buf, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

        buf.seek(0)
        with Image.open(buf) as img:
            img.convert("RGB").save(dst, "PNG")

    print(f"\nダウンロード完了: {image_dir}")


def main():
    import json

    paths = get_paths()
    image_dir = paths["IMAGE_DIR"]

    # episode.json の drive_folder_id を優先、なければ .env の DRIVE_IMAGE_FOLDER_ID を使う
    episode_data = json.loads(paths["INPUT_JSON"].read_text(encoding="utf-8"))
    folder_id = episode_data.get("drive_folder_id", "").strip()

    if not folder_id:
        env = load_env()
        folder_id = env.get("DRIVE_IMAGE_FOLDER_ID", "").strip()

    if not folder_id:
        raise RuntimeError(
            "Drive フォルダIDが見つかりません。\n"
            "episode.json に drive_folder_id を追加するか、\n"
            ".env に DRIVE_IMAGE_FOLDER_ID=<ID> を設定してください。"
        )

    if not CLIENT_SECRET_FILE.exists():
        raise FileNotFoundError(
            f"client_secret.json がありません: {CLIENT_SECRET_FILE}"
        )

    service = get_drive_service()
    download_images(service, folder_id, image_dir)


if __name__ == "__main__":
    main()
