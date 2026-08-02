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
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30
DEFAULT_NATIVE_VOICE_LANG = "en"

# High-Income Monetization Niches
HIGH_INCOME_NICHES = {
    "ai_tools": {
        "name": "AI Tools & Tech Hacks",
        "description": "High-impact 60-second shorts featuring mind-blowing AI productivity tools, prompt tricks, and SaaS hacks that save time or make money.",
        "target_audience": "Tech enthusiasts, entrepreneurs, creators, students",
        "call_to_action": "Comment 'TOOL' below to get the direct links & cheat sheet sent to your DMs!",
        "monetization_focus": "SaaS Affiliate Commissions + Gumroad AI Prompt Guides",
        "cpm_rating": "Very High ($18 - $30 CPM)"
    },
    "wealth_hacks": {
        "name": "Wealth, Money & Passive Income",
        "description": "Short, punchy finance breakdown videos covering passive income systems, digital assets, side hustles, and smart money habits.",
        "target_audience": "Ambitious youth, side-hustlers, finance enthusiasts",
        "call_to_action": "Comment 'MONEY' to get our free passive income starter guide!",
        "monetization_focus": "Finance App Referral Links + Notion Wealth Trackers",
        "cpm_rating": "Ultra High ($25 - $40 CPM)"
    },
    "stoic_mindset": {
        "name": "Stoic Mindset & Executive Success",
        "description": "Cinematic 9:16 vertical shorts with dark aesthetic, philosophical quotes, and actionable life lessons for discipline and focus.",
        "target_audience": "High-performers, builders, ambitious professionals",
        "call_to_action": "Save this Reel & Comment 'GROWTH' for the 30-Day Mindset Planner!",
        "monetization_focus": "E-books, Digital Planners, Self-mastery courses",
        "cpm_rating": "High View Volume + Ebook Sales ($12 - $20 CPM)"
    },
    "productivity_tech": {
        "name": "Productivity & Tech Workflows",
        "description": "Sleek breakdowns of desk setups, Notion workflows, Chrome extensions, and time-saving tech apps.",
        "target_audience": "Remote workers, coders, students, creators",
        "call_to_action": "Comment 'WORKFLOW' for the full template link!",
        "monetization_focus": "Amazon Affiliate Tech Links + Notion Templates",
        "cpm_rating": "High ($15 - $25 CPM)"
    }
}
