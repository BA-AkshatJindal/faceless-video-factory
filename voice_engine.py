import os
import asyncio
import httpx
from gtts import gTTS
import config

# Primary Indian Male Voice Model (100% Free Edge-TTS Engine)
INDIAN_MALE_VOICE = "en-IN-PrabhatNeural"

def generate_audio_edge_tts_indian_male(text: str, output_path: str = "voiceover.mp3") -> str:
    """Generates an authentic, deep Indian Male voiceover using Microsoft Edge-TTS (en-IN-PrabhatNeural) - 100% Free."""
    try:
        import edge_tts
        
        async def _synth():
            communicate = edge_tts.Communicate(text, INDIAN_MALE_VOICE)
            await communicate.save(output_path)

        asyncio.run(_synth())
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"[Voice Engine SUCCESS] Saved authentic Indian Male voiceover ({INDIAN_MALE_VOICE}) to {output_path}")
            return output_path
    except Exception as e:
        print(f"[Voice Engine Warning] Edge-TTS Indian Male error: {e}. Retrying gTTS fallback...")

    # Fallback to gTTS if Edge-TTS fails
    try:
        tts = gTTS(text=text, lang="en", tld="co.in", slow=False)
        tts.save(output_path)
        print(f"[Voice Engine Fallback] Saved gTTS Indian voiceover to {output_path}")
        return output_path
    except Exception as e:
        print(f"[Voice Engine Error] Fallback error: {e}")
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(output_path)
        return output_path

def generate_audio_elevenlabs_indian_male(text: str, output_path: str = "voiceover.mp3", voice_id: str = "IKne3meq5aSn9XLyUdCD") -> str:
    """Generates Indian male voiceover using ElevenLabs API when key is available."""
    api_key = config.ELEVENLABS_API_KEY or os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        return generate_audio_edge_tts_indian_male(text, output_path)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
    }

    response = httpx.post(url, json=data, headers=headers, timeout=30.0)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"[Voice Engine SUCCESS] Saved ElevenLabs Indian Male voiceover to {output_path}")
        return output_path
    else:
        return generate_audio_edge_tts_indian_male(text, output_path)

def create_voiceover(text: str, output_path: str = "voiceover.mp3") -> str:
    """Smart dispatcher for authentic Indian Male voiceover creation."""
    if config.ELEVENLABS_API_KEY or os.environ.get("ELEVENLABS_API_KEY"):
        return generate_audio_elevenlabs_indian_male(text, output_path)
    return generate_audio_edge_tts_indian_male(text, output_path)

if __name__ == "__main__":
    test_text = "Bhai, agar tum 2026 mein bhi saara kaam manually kar rahe ho, toh tum 3 ghante waste kar rahe ho!"
    create_voiceover(test_text, "test_indian_male_voice.mp3")
