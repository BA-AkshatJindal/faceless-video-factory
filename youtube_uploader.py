import os
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import config

def get_authenticated_youtube_service():
    refresh_token = config.YOUTUBE_REFRESH_TOKEN or os.environ.get("YOUTUBE_REFRESH_TOKEN")
    client_id = config.YOUTUBE_CLIENT_ID or os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = config.YOUTUBE_CLIENT_SECRET or os.environ.get("YOUTUBE_CLIENT_SECRET")

    if not refresh_token or not client_id or not client_secret:
        print("[YouTube Uploader] Missing OAuth credentials in environment.")
        return None

    credentials = google.oauth2.credentials.Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )
    return build("youtube", "v3", credentials=credentials)

def upload_short_to_youtube(video_path: str, title: str, description: str, tags: list = None) -> str:
    """Uploads vertical MP4 video to YouTube Shorts using YouTube Data API v3.
    Catches YouTube daily upload quota limits gracefully.
    """
    if not os.path.exists(video_path):
        print(f"[YouTube Uploader Error] Video file {video_path} not found.")
        return ""

    youtube = get_authenticated_youtube_service()
    if not youtube:
        print("[YouTube Uploader Warning] Skipping upload: OAuth credentials missing.")
        return ""

    if tags is None:
        tags = ["Shorts", "AITools", "TechHacks", "HinglishTech", "LikeShareSubscribe"]

    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": "28"  # Science & Technology
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    print(f"[YouTube Uploader] Uploading {video_path} to YouTube Shorts ('{title}')...")
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    try:
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"[YouTube Uploader] Upload progress: {int(status.progress() * 100)}%")

        video_id = response.get("id")
        video_url = f"https://www.youtube.com/shorts/{video_id}"
        print(f"[YouTube Uploader SUCCESS] Published live at {video_url}")
        return video_url

    except Exception as e:
        err_msg = str(e)
        if "uploadLimitExceeded" in err_msg or "400" in err_msg:
            print("[YouTube Uploader Note] YouTube daily upload quota limit reached for today (max ~10-15 Shorts/day for new channels). Quota resets in 24 hours.")
            return "QUOTA_LIMIT_REACHED"
        else:
            print(f"[YouTube Uploader Error] API Upload failed: {e}")
            return ""

if __name__ == "__main__":
    print("Testing YouTube Uploader module...")
