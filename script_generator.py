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
    """Fallback viral script generator when GEMINI_API_KEY is not configured locally."""
    niche_info = config.HIGH_INCOME_NICHES.get(niche_key, config.HIGH_INCOME_NICHES["ai_tools"])
    
    sample_scripts = {
        "ai_tools": {
            "title": "3 Free AI Tools That Feel Illegal to Know",
            "voice_script": "Stop wasting hours doing manual work in 2026. Here are three free AI tools that feel completely illegal to know. First, Perplexity AI. It replaces Google by giving instant answers with real sources. Second, NotebookLM by Google. Upload any PDF or video and it generates a full podcast breakdown in seconds. Third, Claude three point five Sonnet. It writes code and automates workflows ten times faster than ChatGPT. Comment TOOL below to get all free links sent to your DMs!",
            "visual_prompts": ["Futuristic dark AI interface glow", "Person looking shocked at laptop", "Speed productivity graph"],
            "description": "Top 3 secret AI productivity tools for 2026. Automate your workflow today!",
            "hashtags": ["#Shorts", "#AITools", "#TechHacks", "#Productivity", "#Reels"],
            "comment_cta": niche_info["call_to_action"]
        },
        "wealth_hacks": {
            "title": "How to Automate $100/Day Passive Income",
            "voice_script": "Here is how smart entrepreneurs are building automated income streams in 2026. Step one: set up digital assets using AI. Step two: drive zero-cost traffic using short form vertical videos on YouTube and Instagram. Step three: capture leads directly into automated DM funnels using ManyChat. Comment MONEY below to get our free passive income blueprint!",
            "visual_prompts": ["Gold and silver digital charts", "Automated income flow diagram", "Executive luxury desk setup"],
            "description": "Build your automated digital asset pipeline step-by-step.",
            "hashtags": ["#Shorts", "#PassiveIncome", "#Wealth", "#Finance", "#Reels"],
            "comment_cta": niche_info["call_to_action"]
        }
    }
    return sample_scripts.get(niche_key, sample_scripts["ai_tools"])

def generate_viral_script(niche_key: str = "ai_tools") -> dict:
    """Generates a high-retention 60-second video script for YouTube Shorts & Instagram Reels."""
    niche_info = config.HIGH_INCOME_NICHES.get(niche_key, config.HIGH_INCOME_NICHES["ai_tools"])
    
    client = get_gemini_client()
    if not client:
        print("[Script Generator] GEMINI_API_KEY not found in environment. Using high-converting fallback script generator...")
        return generate_offline_fallback(niche_key)

    system_instruction = dedent(f"""
        You are an expert viral content strategist specializing in high-CPM YouTube Shorts and Instagram Reels.
        Your goal is to write a fast-paced, high-retention script designed to drive views and trigger comments for affiliate/lead conversion.

        Niche: {niche_info['name']}
        Target Audience: {niche_info['target_audience']}
        Call to Action (CTA): {niche_info['call_to_action']}

        Script Guidelines:
        1. HOOK (0-3s): Disruptive opening statement that stops the scroll immediately.
        2. VALUE / BODY (3-45s): 3 rapid-fire actionable points or steps. Clear, simple language. Zero filler words.
        3. CALL TO ACTION (45-60s): Clear direction to comment a specific keyword for the link/template.

        Output JSON strictly matching this structure:
        {{
            "title": "Viral Video Title (catchy, max 60 chars)",
            "voice_script": "The exact spoken voiceover text to be read by TTS (around 120-140 words, 45-50 seconds speaking duration). No stage directions in voice script.",
            "visual_prompts": ["Visual prompt 1", "Visual prompt 2", "Visual prompt 3"],
            "description": "YouTube & Instagram description with call to action",
            "hashtags": ["#Shorts", "#AI", "#Productivity", "#Reels"],
            "comment_cta": "{niche_info['call_to_action']}"
        }}
    """).strip()

    prompt = f"Create a viral short video script for the niche: {niche_info['name']}. Focus on a topic that gets high engagement and curiosity."
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

    print("[Script Generator] All Gemini model calls failed. Returning offline fallback script...")
    return generate_offline_fallback(niche_key)

if __name__ == "__main__":
    print("Testing Script Generator...")
    result = generate_viral_script("ai_tools")
    print(json.dumps(result, indent=2))
