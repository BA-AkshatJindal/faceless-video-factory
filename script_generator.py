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
    """Fallback viral script generator in relatable Hinglish when GEMINI_API_KEY is not configured locally."""
    niche_info = config.HIGH_INCOME_NICHES.get(niche_key, config.HIGH_INCOME_NICHES["ai_tools"])
    
    sample_scripts = {
        "ai_tools": {
            "title": "3 Secret AI Tools Jo Google Bhi Chupata Hai",
            "voice_script": "Bhai agar tum 2026 mein bhi saara kaam manually kar rahe ho, toh tum din ke 3 ghante waste kar rahe ho! Aaj main tumhe batane wala hu 3 aise free AI tools jo bilkul illegal feel hote hain. Number one, Perplexity AI. Ye Google ko replace kar deta hai instant source-backed answers ke saath. Number two, NotebookLM by Google. Apni koi bhi PDF ya audio file upload karo aur ye 10 seconds mein full podcast breakdown bana dega! Number three, Claude three point five Sonnet. Ye ChatGPT se 10 times fast coding aur automation karta hai! Direct links ke liye niche comment karo TOOL aur main aapko DMs mein bhej dunga!",
            "visual_prompts": ["Futuristic Indian tech creator avatar", "3D AI glowing hologram dashboard", "High speed automated workflow"],
            "description": "3 Secret Free AI Tools jo har Indian student aur creator ko pata hone chahiye! Automate your work today.",
            "hashtags": ["#Shorts", "#AITools", "#HinglishTech", "#Productivity", "#Reels", "#IndiaTech"],
            "comment_cta": niche_info["call_to_action"]
        },
        "wealth_hacks": {
            "title": "AI Se Daily $100 Passive Income Kaise Banaye",
            "voice_script": "Bhai agar tum ghar baithe automated income banana chahte ho, toh ye 3 steps dhyan se suno. Step number one: AI tools se digital prompt vaults aur templates banao. Step number two: YouTube Shorts aur Instagram Reels se free traffic lao. Step number three: ManyChat DM automation se automated sales convert karo! Comment karo MONEY aur main aapko free starter blueprint bhej dunga!",
            "visual_prompts": ["Digital rupee money growth chart", "Automated income pipeline 3D graphic", "Luxury dark tech desk setup"],
            "description": "Passive income building step by step guide in Hinglish.",
            "hashtags": ["#Shorts", "#PassiveIncome", "#Wealth", "#Finance", "#Reels", "#HinglishTech"],
            "comment_cta": niche_info["call_to_action"]
        }
    }
    return sample_scripts.get(niche_key, sample_scripts["ai_tools"])

def generate_viral_script(niche_key: str = "ai_tools") -> dict:
    """Generates a high-retention 60-second video script in relatable Hinglish (Hindi + English)."""
    niche_info = config.HIGH_INCOME_NICHES.get(niche_key, config.HIGH_INCOME_NICHES["ai_tools"])
    
    client = get_gemini_client()
    if not client:
        print("[Script Generator] GEMINI_API_KEY not found in environment. Using Hinglish fallback script generator...")
        return generate_offline_fallback(niche_key)

    system_instruction = dedent(f"""
        You are an expert viral Indian content strategist specializing in high-converting YouTube Shorts & Instagram Reels.
        You write engaging, high-energy scripts in **Hinglish (Hindi + English mixed, written strictly in clean English/Roman script)**.

        Niche: {niche_info['name']}
        Target Audience: Indian students, freshers, tech enthusiasts, creators
        Call to Action (CTA): {niche_info['call_to_action']}

        CRITICAL SCRIPT RULES:
        1. LANGUAGE: Use **Hinglish** (Hindi spoken phrases like "Bhai, agar tum...", "bilkul free...", "kaam manually...", "DMs me bhej dunga") written ONLY in Roman English letters!
        2. HOOK (0-3s): High-curiosity scroll-stopping Indian tech hook.
        3. BODY (3-45s): 3 rapid-fire actionable points with high energy. Zero filler words.
        4. CTA (45-60s): Clear direction to comment a specific keyword for the link/template.

        Output JSON strictly matching this structure:
        {{
            "title": "Catchy Hinglish Title (max 60 chars)",
            "voice_script": "The exact spoken Hinglish text in English letters (120-140 words, 45-50 seconds duration). No stage directions.",
            "visual_prompts": ["Visual prompt 1", "Visual prompt 2", "Visual prompt 3"],
            "description": "Hinglish description with call to action",
            "hashtags": ["#Shorts", "#AITools", "#HinglishTech", "#Reels", "#IndiaTech"],
            "comment_cta": "{niche_info['call_to_action']}"
        }}
    """).strip()

    prompt = f"Create a viral short video script in Hinglish for the niche: {niche_info['name']}. Focus on a relatable tech/AI problem that Indian youth care about."
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

    print("[Script Generator] All Gemini model calls failed. Returning Hinglish fallback script...")
    return generate_offline_fallback(niche_key)

if __name__ == "__main__":
    print("Testing Hinglish Script Generator...")
    result = generate_viral_script("ai_tools")
    print(json.dumps(result, indent=2))
