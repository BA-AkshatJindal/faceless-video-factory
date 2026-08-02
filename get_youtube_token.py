import os
import sys
import json

# Force UTF-8 stdout for Windows compatibility
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    print("\n========================================================")
    print(" [*] YOUTUBE OAUTH REFRESH TOKEN GENERATOR")
    print("========================================================\n")
    
    client_secret_file = "client_secret.json"
    if not os.path.exists(client_secret_file):
        print(f"[!] '{client_secret_file}' not found in this directory.\n")
        return

    try:
        flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
        auth_url, _ = flow.authorization_url(prompt="consent")
        
        print("Please open the following link in your browser to sign in:")
        print(f"\n{auth_url}\n")

        # Run local web server to complete OAuth flow
        creds = flow.run_local_server(port=8080, open_browser=True)

        with open(client_secret_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            info = data.get("installed") or data.get("web") or {}

        client_id = info.get("client_id")
        client_secret = info.get("client_secret")
        refresh_token = creds.refresh_token

        print("\n========================================================")
        print(" [SUCCESS] AUTHORIZATION COMPLETED!")
        print("========================================================\n")
        print(f"YOUTUBE_CLIENT_ID     : {client_id}")
        print(f"YOUTUBE_CLIENT_SECRET : {client_secret}")
        print(f"YOUTUBE_REFRESH_TOKEN : {refresh_token}")
        print("\n========================================================\n")

        # Save credentials to json file locally for easy reference
        creds_data = {
            "YOUTUBE_CLIENT_ID": client_id,
            "YOUTUBE_CLIENT_SECRET": client_secret,
            "YOUTUBE_REFRESH_TOKEN": refresh_token
        }
        with open("youtube_creds.json", "w", encoding="utf-8") as f:
            json.dump(creds_data, f, indent=2)

        print("[!] Credentials saved to youtube_creds.json (gitignored).")

    except Exception as e:
        print(f"[Error] Failed authorization flow: {e}")

if __name__ == "__main__":
    main()
