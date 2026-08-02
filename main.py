import os
import sys
import json
import argparse

# Force UTF-8 stdout for Windows compatibility
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from script_generator import generate_viral_script
from voice_engine import create_voiceover
from video_engine import render_short_video
from youtube_uploader import upload_short_to_youtube
from insta_uploader import publish_reel_to_instagram
import config

def run_faceless_pipeline(niche_key: str = "ai_tools"):
    print(f"\n========================================================")
    print(f" [*] FACELESS VIDEO & REVENUE ENGINE STARTING")
    print(f" Selected Niche: {niche_key.upper()}")
    print(f"========================================================\n")

    # Step 1: Generate AI Script & Metadata
    print(" [1/4] Generating Viral Script with Gemini AI...")
    script_data = generate_viral_script(niche_key)
    print(f"  Title: {script_data.get('title')}")
    print(f"  CTA:   {script_data.get('comment_cta')}\n")

    # Save metadata locally
    with open("latest_script.json", "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=2, ensure_ascii=False)

    # Step 2: Voiceover Synthesis
    print(" [2/4] Synthesizing Voiceover Audio...")
    voice_path = create_voiceover(script_data["voice_script"], "voiceover.mp3")

    # Step 3: Render 9:16 Vertical Video
    print(" [3/4] Rendering 9:16 Vertical Short/Reel Video...")
    video_output = render_short_video(voice_path, script_data, "output_short.mp4")

    # Step 4: Auto-Publishing to YouTube & Instagram
    print(" [4/4] Publishing Video across Revenue Channels...")
    title = script_data.get("title", "Viral Short")
    desc = f"{script_data.get('description', '')}\n\n{script_data.get('comment_cta', '')}\n\n" + " ".join(script_data.get("hashtags", []))

    yt_id = upload_short_to_youtube(video_output, title, desc, script_data.get("hashtags", []))
    
    # Note: Instagram Graph API requires public video URL; in local test mode it logs simulation
    ig_id = publish_reel_to_instagram("https://example.com/output_short.mp4", desc)

    print("\n========================================================")
    print(" [SUCCESS] PIPELINE COMPLETED SUCCESSFULLY!")
    print(f" YouTube Short ID: {yt_id}")
    print(f" Instagram Reel ID: {ig_id}")
    print("========================================================\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Faceless AI Video Engine")
    parser.add_argument("--niche", type=str, default="ai_tools", choices=["ai_tools", "wealth_hacks", "stoic_mindset", "productivity_tech"], help="Select revenue niche")
    args = parser.parse_args()

    run_faceless_pipeline(args.niche)
