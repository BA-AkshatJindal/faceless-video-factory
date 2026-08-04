import os
import sys

# Ensure UTF-8 console output on Windows & Linux
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import argparse
import config
import script_generator
import voice_engine
import video_engine
import youtube_uploader
import insta_uploader
import marketing_agent

def run_faceless_factory_pipeline(niche_key: str = "ai_tools"):
    print("=====================================================")
    print("[*] STARTING AUTOMATED FACELESS VIDEO & REVENUE ENGINE")
    print(f"Target Niche: {niche_key}")
    print("=====================================================")

    if niche_key not in config.HIGH_INCOME_NICHES:
        niche_key = "ai_tools"

    # Step 1: Generate Script
    print("\n[Step 1/5] Generating Metro City Hinglish viral script...")
    script_data = script_generator.generate_viral_script(niche_key)
    print(f"-> Title Generated: {script_data.get('title')}")

    # Step 2: YouTube Algorithm Marketing Agent Optimization
    print("\n[Step 2/5] Running YouTube SEO & Marketing Agent...")
    seo_metadata = marketing_agent.optimize_youtube_metadata(
        topic=script_data.get("title", "AI Tools"),
        raw_script=script_data.get("voice_script", "")
    )
    
    script_data["title"] = seo_metadata.get("seo_title", script_data.get("title"))
    script_data["description"] = seo_metadata.get("seo_description", script_data.get("description"))
    script_data["hashtags"] = seo_metadata.get("hashtags", script_data.get("hashtags"))
    print(f"-> Optimized High-CTR Title: {script_data['title']}")

    # Step 3: Synthesize Indian Male Voiceover
    print("\n[Step 3/5] Synthesizing Indian Male Voiceover (en-IN-PrabhatNeural)...")
    voiceover_file = "voiceover.mp3"
    voice_path = voice_engine.create_voiceover(script_data["voice_script"], voiceover_file)
    print(f"-> Voiceover saved to {voice_path}")

    # Step 4: Render Full-Screen 9:16 Video
    print("\n[Step 4/5] Rendering 100% Full-Screen 9:16 vertical video...")
    final_video_file = "final_short.mp4"
    video_path = video_engine.render_short_video(voice_path, script_data, final_video_file)
    print(f"-> Video rendered to {video_path}")

    # Step 5: Upload to YouTube & Instagram Reels
    print("\n[Step 5/5] Publishing live to YouTube Shorts & Instagram Reels...")
    title = script_data.get("title", "AI Tools Hack")
    desc = script_data.get("description", "")
    tags = script_data.get("hashtags", ["Shorts", "AITools"])

    yt_result = youtube_uploader.upload_short_to_youtube(video_path, title, desc, tags)
    print(f"-> YouTube Status: {yt_result}")

    insta_result = insta_uploader.upload_reel_to_instagram(video_path, script_data)
    print(f"-> Instagram Status: {insta_result}")

    print("\n=====================================================")
    print("[*] ENGINE PIPELINE EXECUTION COMPLETE!")
    print("=====================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Faceless Shorts Engine")
    parser.add_argument("--niche", type=str, default="ai_tools", help="Revenue Niche Key")
    args, unknown = parser.parse_known_args()
    
    selected_niche = args.niche if args.niche in config.HIGH_INCOME_NICHES else "ai_tools"
    run_faceless_factory_pipeline(selected_niche)
