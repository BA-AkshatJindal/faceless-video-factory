import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    print("\n========================================================")
    print(" 🔴 YOUTUBE OAUTH REFRESH TOKEN GENERATOR")
    print("========================================================\n")
    
    client_secret_file = "client_secret.json"
    if not os.path.exists(client_secret_file):
        print(f"[!] '{client_secret_file}' not found in this directory.\n")
        print("Quick Setup Instructions (Takes 2 minutes):")
        print(" 1. Go to Google Cloud Console: https://console.cloud.google.com/")
        print(" 2. Click 'Create Project' -> Name it 'Faceless Shorts'")
        print(" 3. Search for 'YouTube Data API v3' and click 'Enable'")
        print(" 4. Go to 'Credentials' -> 'Create Credentials' -> 'OAuth client ID'")
        print("    (Application type: Desktop App)")
        print(" 5. Download the JSON file, rename it to 'client_secret.json', and save it in this folder.\n")
        print("Then run: python get_youtube_token.py\n")
        return

    try:
        flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
        creds = flow.run_local_server(port=8080)

        with open(client_secret_file, "r") as f:
            data = json.load(f)
            info = data.get("installed") or data.get("web") or {}

        print("\n========================================================")
        print(" ✅ SUCCESS! Copy these 3 values to GitHub Secrets:")
        print(" https://github.com/BA-AkshatJindal/faceless-video-factory/settings/secrets/actions")
        print("========================================================\n")
        print(f"YOUTUBE_CLIENT_ID     : {info.get('client_id')}")
        print(f"YOUTUBE_CLIENT_SECRET : {info.get('client_secret')}")
        print(f"YOUTUBE_REFRESH_TOKEN : {creds.refresh_token}")
        print("\n========================================================\n")
    except Exception as e:
        print(f"[Error] Failed authorization flow: {e}")

if __name__ == "__main__":
    main()
