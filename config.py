import os
from dotenv import load_dotenv

load_dotenv()

# Central API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")

# YouTube Credentials
YOUTUBE_CLIENT_SECRET_FILE = os.getenv("YOUTUBE_CLIENT_SECRET_FILE", "client_secret.json")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")

# Instagram Meta Graph API Credentials
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "")

# Render Settings
VIDEO_WIDTH = 720
VIDEO_HEIGHT = 1280
VIDEO_FPS = 24
DEFAULT_NATIVE_VOICE_LANG = "en"

# High-Income Monetization Niches (Hinglish & Global Indian Audience Calibrated)
HIGH_INCOME_NICHES = {
    "ai_tools": {
        "name": "AI Tools & Tech Hacks (Hinglish)",
        "description": "High-energy 60-second shorts in relatable Hinglish (Hindi + English) featuring secret AI productivity tools, prompt tricks, and SaaS hacks.",
        "target_audience": "Indian tech enthusiasts, developers, students, creators",
        "call_to_action": "Comment 'TOOL' karke bolo, main saare free links aapke DMs me bhej dunga!",
        "monetization_focus": "SaaS Affiliate Commissions + Gumroad AI Prompt Guides",
        "cpm_rating": "Very High ($18 - $30 CPM)"
    },
    "wealth_hacks": {
        "name": "Wealth, Money & Passive Income (Hinglish)",
        "description": "Short, punchy finance breakdown videos in Hinglish covering passive income systems, digital assets, side hustles, and smart money habits.",
        "target_audience": "Ambitious youth, side-hustlers, finance enthusiasts",
        "call_to_action": "Comment 'MONEY' karo free passive income starter guide ke liye!",
        "monetization_focus": "Finance App Referral Links + Notion Wealth Trackers",
        "cpm_rating": "Ultra High ($25 - $40 CPM)"
    },
    "stoic_mindset": {
        "name": "Stoic Mindset & Executive Success (Hinglish)",
        "description": "Cinematic 9:16 vertical shorts in Hinglish with dark aesthetic, philosophical quotes, and actionable life lessons for discipline and focus.",
        "target_audience": "High-performers, builders, ambitious professionals",
        "call_to_action": "Comment 'GROWTH' karo 30-Day Mindset Planner ke liye!",
        "monetization_focus": "E-books, Digital Planners, Self-mastery courses",
        "cpm_rating": "High View Volume + Ebook Sales ($12 - $20 CPM)"
    },
    "productivity_tech": {
        "name": "Productivity & Tech Workflows (Hinglish)",
        "description": "Sleek breakdowns in Hinglish of desk setups, Notion workflows, Chrome extensions, and time-saving tech apps.",
        "target_audience": "Remote workers, coders, students, creators",
        "call_to_action": "Comment 'WORKFLOW' karo full template link ke liye!",
        "monetization_focus": "Amazon Affiliate Tech Links + Notion Templates",
        "cpm_rating": "High ($15 - $25 CPM)"
    }
}
