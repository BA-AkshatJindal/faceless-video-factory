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
    """Fallback viral script generator in Metro City Techie Hinglish with mandatory Like, Share, Comment & Subscribe CTA."""
    niche_info = config.HIGH_INCOME_NICHES.get(niche_key, config.HIGH_INCOME_NICHES["ai_tools"])
    
    sample_scripts = {
        "ai_tools": {
            "title": "3 Secret AI Tools Google Is Hiding From You",
            "voice_script": "Bro, if you are still doing your daily research manually in 2026, you are literally wasting 3 hours every single day! Today I am going to reveal 3 secret AI tools jo bilkul game-changing hain. Tool number one is Perplexity AI. It literally replaces Google search with instant source-backed answers. Tool number two is NotebookLM by Google. Upload any PDF or video and ye 10 seconds mein full podcast breakdown generate kar dega! Tool number three is Claude three point five Sonnet. It automates coding and workflows ten times faster than ChatGPT! Drop a comment TOOL below and main saare direct free links aapke DMs me bhej dunga! Make sure to Like, Share with your tech friends, and Subscribe for daily AI hacks!",
            "visual_prompts": ["Photorealistic Indian techie host studio", "3D AI glowing hologram dashboard", "High speed automated workflow"],
            "description": "3 Secret Free AI Tools every techie and student needs in 2026! 🔥 Like, Share, Comment 'TOOL' & Subscribe for daily AI & tech hacks!",
            "hashtags": ["#Shorts", "#AITools", "#MetroTech", "#Productivity", "#Reels", "#LikeShareSubscribe"],
            "comment_cta": niche_info["call_to_action"]
        },
        "wealth_hacks": {
            "title": "How to Automate $100/Day Passive Income Stream",
            "voice_script": "Bro, if you want to build automated passive income from home, follow these 3 simple steps. Step number one: Build digital prompt vaults and templates using AI. Step number two: Generate zero-cost organic traffic using short form vertical videos on YouTube and Instagram. Step number three: Capture leads automatically using ManyChat DM workflows. Drop a comment MONEY below and main aapko free passive income starter guide bhej dunga! Make sure to Like, Share and Subscribe for daily wealth hacks!",
            "visual_prompts": ["Digital rupee money growth chart", "Automated income pipeline 3D graphic", "Luxury dark tech desk setup"],
            "description": "Passive income building step by step guide. 🔥 Like, Share, Comment 'MONEY' & Subscribe for daily wealth & finance hacks!",
            "hashtags": ["#Shorts", "#PassiveIncome", "#Wealth", "#Finance", "#Reels", "#LikeShareSubscribe"],
            "comment_cta": niche_info["call_to_action"]
        }
    }
    return sample_scripts.get(niche_key, sample_scripts["ai_tools"])

def generate_viral_script(niche_key: str = "ai_tools") -> dict:
    """Generates a high-retention 60-second video script with mandatory Like, Share, Comment & Subscribe CTA."""
    niche_info = config.HIGH_INCOME_NICHES.get(niche_key, config.HIGH_INCOME_NICHES["ai_tools"])
    
    client = get_gemini_client()
    if not client:
        print("[Script Generator] GEMINI_API_KEY not found in environment. Using Metro City Hinglish fallback script generator...")
        return generate_offline_fallback(niche_key)

    system_instruction = dedent(f"""
        You are an expert Metro City Indian tech creator (Bangalore / Mumbai / Gurgaon techie vibe).
        You write high-energy, fast-paced scripts in **Metro City Hinglish (70% professional English + 30% conversational Hindi slang)**.

        Niche: {niche_info['name']}
        Target Audience: Metro techies, developers, freshers, product managers, creators

        CRITICAL MANDATORY ENDING CTA RULE:
        Every script MUST strictly end with this call-to-action:
        "Drop a comment [KEYWORD] below and main saare direct free links aapke DMs me bhej dunga! Make sure to Like, Share with your friends, and Subscribe for daily AI hacks!"

        Output JSON strictly matching this structure:
        {{
            "title": "Catchy Metro Tech Title (max 60 chars)",
            "voice_script": "The exact spoken Metro Hinglish text in English letters (120-140 words, 45-50 seconds duration). Must end with Like, Share, Comment & Subscribe CTA. No stage directions.",
            "visual_prompts": ["Visual prompt 1", "Visual prompt 2", "Visual prompt 3"],
            "description": "Metro Tech description with '🔥 Like, Share, Comment & Subscribe for daily AI hacks!'",
            "hashtags": ["#Shorts", "#AITools", "#MetroTech", "#Reels", "#LikeShareSubscribe"],
            "comment_cta": "{niche_info['call_to_action']}"
        }}
    """).strip()

    prompt = f"Create a viral short video script in Metro City Hinglish (70% English + 30% Hindi) for the niche: {niche_info['name']}. Ensure it ends with Like, Share, Comment & Subscribe CTA."
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
            data = json.loads(response.text)
            return data
        except Exception as e:
            print(f"[Warning] Failed model {model_name}: {e}. Retrying fallback...")

    print("[Script Generator] All Gemini model calls failed. Returning Metro City Hinglish fallback script...")
    return generate_offline_fallback(niche_key)

if __name__ == "__main__":
    print("Testing Script Generator with Like Share Comment Subscribe CTA...")
    result = generate_viral_script("ai_tools")
    print(json.dumps(result, indent=2))
