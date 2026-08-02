import os
import time
import httpx
import config

def publish_reel_via_instagrapi(video_path: str, caption: str) -> str:
    """Publishes a video directly to Instagram Reels using instagrapi (NO Facebook account needed)."""
    username = os.environ.get("INSTAGRAM_USERNAME") or config.INSTAGRAM_ACCESS_TOKEN
    password = os.environ.get("INSTAGRAM_PASSWORD") or config.INSTAGRAM_ACCOUNT_ID

    if not username or not password:
        print("[Instagram Uploader] Missing INSTAGRAM_USERNAME / INSTAGRAM_PASSWORD. Skipping live Instagram upload.")
        return ""

    try:
        print(f"[Instagram Uploader] Logging into Instagram as @{username} via instagrapi...")
        from instagrapi import Client

        cl = Client()
        cl.login(username, password)

        print(f"[Instagram Uploader] Uploading {video_path} as Instagram Reel...")
        media = cl.clip_upload(video_path, caption=caption)
        
        media_id = str(media.pk)
        print(f"[Instagram Uploader SUCCESS] Published Reel live to @{username}! Media PK: {media_id}")
        return media_id

    except Exception as e:
        print(f"[Instagram Uploader Error] instagrapi upload error: {e}")
        return ""

def upload_reel_to_instagram(video_path: str, script_data: dict) -> str:
    """Smart Instagram Reel Uploader supporting both instagrapi (Direct Login) and Meta Graph API."""
    title = script_data.get("title", "")
    desc = script_data.get("description", "")
    hashtags = " ".join(script_data.get("hashtags", []))
    caption = f"{title}\n\n{desc}\n\n{hashtags}"

    # Try Direct Username/Password instagrapi Upload (NO Facebook required)
    result = publish_reel_via_instagrapi(video_path, caption)
    if result:
        return result

    # Fallback to Meta Graph API if access token provided
    access_token = config.INSTAGRAM_ACCESS_TOKEN or os.environ.get("INSTAGRAM_ACCESS_TOKEN")
    account_id = config.INSTAGRAM_ACCOUNT_ID or os.environ.get("INSTAGRAM_ACCOUNT_ID")

    if access_token and account_id:
        try:
            print("[Instagram Uploader] Falling back to Meta Graph API upload...")
            container_url = f"https://graph.facebook.com/v20.0/{account_id}/media"
            payload = {
                "media_type": "REELS",
                "caption": caption,
                "access_token": access_token
            }
            res = httpx.post(container_url, data=payload, timeout=30.0)
            data = res.json()
            if "id" in data:
                return data["id"]
        except Exception as e:
            print(f"[Instagram Uploader Meta API Error]: {e}")

    return ""

if __name__ == "__main__":
    print("Testing Instagram Uploader module...")
