import os
import json
import random
from textwrap import dedent
from google import genai
from google.genai import types
import config

def get_gemini_client():
    api_key = config.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def generate_offline_fallback(niche_key: str) -> dict:
    """Fallback viral script generator in Metro City Techie Hinglish with cinematic prompts."""
    niche_info = config.HIGH_INCOME_NICHES.get(niche_key, config.HIGH_INCOME_NICHES["ai_tools"])
    
    sample_scripts = {
        "ai_tools": {
            "title": "3 Secret AI Tools Google Is Hiding From You",
            "voice_script": "Bro, if you are still doing your daily research manually in 2026, you are literally wasting 3 hours every single day! Today I am going to reveal 3 secret AI tools jo bilkul game-changing hain. Tool number one is Perplexity AI. It literally replaces Google search with instant source-backed answers. Tool number two is NotebookLM by Google. Upload any PDF or video and ye 10 seconds mein full podcast breakdown generate kar dega! Tool number three is Claude three point five Sonnet. It automates coding and workflows ten times faster than ChatGPT! Drop a comment TOOL below and main saare direct free links aapke DMs me bhej dunga! Make sure to Like, Share with your tech friends, and Subscribe for daily AI hacks!",
            "visual_prompts": [
                "Cinematic realistic 4K portrait of young Indian tech enthusiast developer in dark mode workspace with blue purple RGB lighting typing on Mac keyboard surrounded by multiple coding monitors",
                "Floating glassmorphism UI card of Perplexity AI search dashboard with glowing cyan HUD graphics",
                "Over the shoulder shot of NotebookLM podcast generator interface with animated digital audio waves"
            ],
            "description": "3 Secret Free AI Tools every techie and student needs in 2026! 🔥 Like, Share, Comment 'TOOL' & Subscribe for daily AI & tech hacks!",
            "hashtags": ["#Shorts", "#AITools", "#MetroTech", "#Productivity", "#Reels", "#LikeShareSubscribe"],
            "comment_cta": niche_info["call_to_action"]
        }
    }
    return sample_scripts.get(niche_key, sample_scripts["ai_tools"])

def generate_viral_script(niche_key: str = "ai_tools") -> dict:
    """Generates a high-retention video script with cinematic visual prompt blueprints."""
    niche_info = config.HIGH_INCOME_NICHES.get(niche_key, config.HIGH_INCOME_NICHES["ai_tools"])
    
    client = get_gemini_client()
    if not client:
        return generate_offline_fallback(niche_key)

    system_instruction = dedent(f"""
        You are an expert Metro City Indian tech creator (Bangalore / Mumbai / Gurgaon techie vibe).
        You write high-energy scripts in **Metro City Hinglish (70% professional English + 30% conversational Hindi slang)**.

        Visual Style Blueprint:
        - Cinematic 4K, dark mode workspace, blue/purple RGB ambient lighting.
        - Young Indian tech lover boy host in sleek ergonomic chair with Mac Studio & multiple code monitors.
        - Floating glassmorphism UI mockups, clean logo icon overlays, and dynamic HUD feature highlights.

        CRITICAL MANDATORY ENDING CTA RULE:
        Every script MUST strictly end with:
        "Drop a comment [KEYWORD] below and main saare direct free links aapke DMs me bhej dunga! Make sure to Like, Share with your friends, and Subscribe for daily AI hacks!"

        Output JSON strictly matching this structure:
        {{
            "title": "Catchy Metro Tech Title (max 60 chars)",
            "voice_script": "The exact spoken Metro Hinglish text in English letters (120-140 words). Must end with Like, Share, Comment & Subscribe CTA.",
            "visual_prompts": ["Cinematic prompt for scene 1", "Cinematic prompt for scene 2", "Cinematic prompt for scene 3"],
            "description": "Metro Tech description with '🔥 Like, Share, Comment & Subscribe for daily AI hacks!'",
            "hashtags": ["#Shorts", "#AITools", "#MetroTech", "#Reels", "#LikeShareSubscribe"],
            "comment_cta": "{niche_info['call_to_action']}"
        }}
    """).strip()

    prompt = f"Create a viral short video script in Metro City Hinglish for niche: {niche_info['name']}. Include cinematic visual prompts with tool overlays."
    models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.7,
                )
            )
            return json.loads(response.text)
        except Exception:
            pass

    return generate_offline_fallback(niche_key)

if __name__ == "__main__":
    result = generate_viral_script("ai_tools")
    print(json.dumps(result, indent=2))
