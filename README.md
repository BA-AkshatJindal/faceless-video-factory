# 🎬 Faceless AI Video & Revenue Engine (YouTube & Instagram)

> **An Autonomous, 100% Free-Tier Engine that generates, renders, and auto-publishes high-converting 9:16 vertical Shorts & Reels to drive YouTube AdSense, Affiliate Sales, and Automated Instagram DM Funnels.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Execution](https://img.shields.io/badge/Execution-GitHub%20Actions-blueviolet.svg)]()
[![Cost](https://img.shields.io/badge/Running%20Cost-%240.00%2Fmo%20(Free%20Tier)-brightgreen.svg)]()

---

## 🎯 Strategic Purpose: Pure Income & Traffic Engine

While your LinkedIn engine builds your executive personal brand, **this engine is dedicated to high-volume revenue generation** across YouTube Shorts & Instagram Reels.

### 💰 Revenue Channels Built-In:
1. **YouTube AdSense & Shorts Monetization** (High CPM content).
2. **Affiliate Marketing Links** (Automatically placed in YouTube Descriptions & Instagram DMs).
3. **Instagram DM Lead Conversion (ManyChat Integration)** (Instant delivery of e-books, Notion templates, and SaaS tools).
4. **Faceless Sponsorship Deals** (Automated video slots for brand partners).

---

## 🏗️ System Architecture

```
 ⏰ TWICE DAILY EXECUTION (GitHub Actions Cron / Manual Dispatch)
 └── Trigger: python main.py --niche ai_tools
```

```
┌────────────────────────────────────────────────────────┐
│ 1. VIRAL SCRIPT & METADATA GENERATOR (Gemini AI)       │
│    • High-retention 3-part hook strategy                │
│    • Word-timed voice script + thumbnail concept       │
│    • Dynamic niche templates (AI Tools, Wealth, Tech)  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 2. VOICE & AUDIO SYNTHESIS ENGINE                      │
│    • High-clarity TTS voiceover (gTTS / ElevenLabs)    │
│    • Dynamic duration matching & audio normalization   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 3. PROGRAMMATIC 9:16 VIDEO RENDERER (MoviePy + Pillow) │
│    • FLUX / Pexels high-impact visual background      │
│    • Burned-in, centered animated Karaoke subtitles  │
│    • HD 1080x1920 MP4 video rendering                   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 4. AUTO-PUBLISHING & MONETIZATION FUNNEL               │
│    ├─ 🔴 YouTube Shorts API (google-api-python-client) │
│    ├─ 📸 Instagram Reels API (Meta Graph API)          │
│    └─ 💬 ManyChat DM Trigger (Captures leads to cash)  │
└────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
faceless-video-factory/
├── config.py              # Central settings, niche options, API secrets
├── script_generator.py    # Gemini AI viral script generator
├── voice_engine.py        # TTS voice synthesis module
├── video_engine.py        # MoviePy 9:16 Shorts/Reels video composer
├── youtube_uploader.py    # YouTube Data API v3 upload engine
├── insta_uploader.py      # Meta Graph API Reels uploader
├── main.py                # Main orchestration pipeline
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
```

---

## ⚙️ Quick Start Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables (`.env`)
```env
GEMINI_API_KEY="your_gemini_api_key"
YOUTUBE_CLIENT_SECRET_FILE="client_secret.json"
INSTAGRAM_ACCESS_TOKEN="your_meta_graph_token"
INSTAGRAM_ACCOUNT_ID="your_ig_business_id"
ELEVENLABS_API_KEY="optional_elevenlabs_key"
```

### 3. Run Pipeline Manually
```bash
python main.py --niche ai_tools
```
