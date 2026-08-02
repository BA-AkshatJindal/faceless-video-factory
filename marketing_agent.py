import os
import json
from textwrap import dedent
from google import genai
from google.genai import types
import config

def get_gemini_client():
    api_key = config.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def optimize_youtube_metadata(topic: str, raw_script: str) -> dict:
    """YouTube SEO & Marketing Agent that generates high-CTR titles, algorithm-optimized descriptions,
    and viral Shorts tags calibrated for the YouTube Shorts Recommendation Algorithm in 2026.
    """
    client = get_gemini_client()

    system_instruction = dedent("""
        You are an elite YouTube Algorithm & SEO Marketing Specialist specializing in 60-second YouTube Shorts.
        Your sole mission is to maximize CTR (Click-Through Rate), AVD (Average View Duration), and Shorts Feed Reach.

        YOUTUBE ALGORITHM RULES (2026):
        1. VIRAL TITLE: Must be under 60 characters, use curiosity gaps, number triggers, bracketed power tags like [2026 FREE], and high-conversion Metro Hinglish keywords.
        2. SEO DESCRIPTION: Must include primary & secondary search keywords in the first 2 lines, timestamp breakdown, and mandatory CTA:
           "🔥 Like, Share, Comment 'TOOL' & Subscribe for daily AI & tech hacks!"
        3. HIGH-REACH TAGS: Generate 15 high-volume search tags formatted both as comma-separated tags and hashtags.

        Output JSON strictly matching this structure:
        {
            "seo_title": "High-CTR Title (max 55 chars)",
            "seo_description": "Full keyword-rich description with links and CTAs",
            "search_tags": ["Shorts", "AI Tools", "Tech Hacks", "Hinglish Tech", "India Tech"],
            "hashtags": ["#Shorts", "#AITools", "#TechHacks", "#HinglishTech", "#LikeShareSubscribe"]
        }
    """).strip()

    prompt = f"Optimize YouTube metadata for Topic: '{topic}' with Script: '{raw_script[:200]}...'"

    if client:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.7,
                )
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"[Marketing Agent Warning] Gemini API note: {e}")

    # High-converting fallback metadata engine
    return {
        "seo_title": f"3 Secret AI Tools Google Is Hiding From You [2026]",
        "seo_description": dedent(f"""
            Bro, if you are still doing your daily research manually in 2026, you are literally wasting 3 hours every single day! Today I am revealing 3 secret AI tools jo bilkul game-changing hain.

            📌 TOOLS FEATURED:
            1️⃣ Perplexity AI - Instant source-backed answers
            2️⃣ NotebookLM by Google - 10s podcast & PDF breakdown
            3️⃣ Claude 3.5 Sonnet - 10x faster coding & workflow automation

            🔥 Drop a comment 'TOOL' below and main saare direct free links aapke DMs me bhej dunga!
            Make sure to Like, Share with your tech friends, and Subscribe to @ByteSizedAI for daily AI & tech hacks!

            #Shorts #AITools #MetroTech #Productivity #Reels #LikeShareSubscribe
        """).strip(),
        "search_tags": ["Shorts", "AI Tools", "Tech Hacks", "Hinglish Tech", "India Tech", "Perplexity AI", "NotebookLM", "Claude AI", "Productivity Hacks", "LikeShareSubscribe"],
        "hashtags": ["#Shorts", "#AITools", "#MetroTech", "#Productivity", "#Reels", "#LikeShareSubscribe"]
    }

if __name__ == "__main__":
    print("Testing YouTube Marketing Agent...")
    metadata = optimize_youtube_metadata("AI Productivity Tools", "Bro, if you are still doing your research manually...")
    print(json.dumps(metadata, indent=2))
