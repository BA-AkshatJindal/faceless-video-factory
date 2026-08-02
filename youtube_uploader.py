import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import config

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_youtube_service():
    """Initializes YouTube API client using refresh token or client secret."""
    refresh_token = config.YOUTUBE_REFRESH_TOKEN or os.environ.get("YOUTUBE_REFRESH_TOKEN")
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")

    if refresh_token and client_id and client_secret:
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES
        )
        return build("youtube", "v3", credentials=creds)
    else:
        print("[YouTube Uploader] Missing YouTube API Credentials in environment. Skipping live upload.")
        return None

def upload_short_to_youtube(video_file_path: str, title: str, description: str, tags: list = None) -> str:
    """Uploads vertical MP4 short video to YouTube Shorts."""
    youtube = get_youtube_service()
    if not youtube:
        print(f"[YouTube Uploader SIMULATION] Would upload {video_file_path} with Title: {title}")
        return "simulation_video_id"

    if tags is None:
        tags = ["Shorts", "AI", "Tech", "Viral"]

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

    media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    
    print(f"[YouTube Uploader] Uploading {video_file_path} to YouTube Shorts...")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()

    video_id = response.get("id")
    print(f"[YouTube Uploader SUCCESS] Uploaded! Video URL: https://youtube.com/shorts/{video_id}")
    return video_id

if __name__ == "__main__":
    print("Testing YouTube Uploader interface...")
