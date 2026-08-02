import os
import time
import httpx
import config

def publish_reel_to_instagram(video_url: str, caption: str) -> str:
    """Publishes a video URL as an Instagram Reel using the Meta Graph API."""
    access_token = config.INSTAGRAM_ACCESS_TOKEN or os.environ.get("INSTAGRAM_ACCESS_TOKEN")
    account_id = config.INSTAGRAM_ACCOUNT_ID or os.environ.get("INSTAGRAM_ACCOUNT_ID")

    if not access_token or not account_id:
        print("[Instagram Uploader] Missing Meta Graph API Credentials. Skipping live Instagram upload.")
        print(f"[Instagram Uploader SIMULATION] Would upload video URL {video_url} with Caption:\n{caption[:80]}...")
        return "simulation_ig_media_id"

    # Step 1: Create Container for Reel
    container_url = f"https://graph.facebook.com/v20.0/{account_id}/media"
    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "access_token": access_token
    }

    print(f"[Instagram Uploader] Creating Reel container for account {account_id}...")
    res = httpx.post(container_url, data=payload, timeout=30.0)
    data = res.json()

    if "id" not in data:
        print(f"[Instagram Uploader Error] Failed container creation: {data}")
        return ""

    creation_id = data["id"]
    print(f"[Instagram Uploader] Container created (ID: {creation_id}). Checking status...")

    # Wait for Instagram processing
    status_url = f"https://graph.facebook.com/v20.0/{creation_id}"
    for _ in range(10):
        time.sleep(5)
        status_res = httpx.get(status_url, params={"fields": "status_code", "access_token": access_token}).json()
        status_code = status_res.get("status_code")
        print(f"  Container status: {status_code}")
        if status_code == "FINISHED":
            break

    # Step 2: Publish Container
    publish_url = f"https://graph.facebook.com/v20.0/{account_id}/media_publish"
    pub_res = httpx.post(publish_url, data={"creation_id": creation_id, "access_token": access_token}).json()
    
    media_id = pub_res.get("id", "")
    print(f"[Instagram Uploader SUCCESS] Published Reel! Media ID: {media_id}")
    return media_id

if __name__ == "__main__":
    print("Testing Instagram Uploader interface...")
