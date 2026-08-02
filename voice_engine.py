import os
import httpx
from gtts import gTTS
import config

def generate_audio_gtts_indian(text: str, output_path: str = "voiceover.mp3") -> str:
    """Generates authentic Indian accent voiceover using Google TTS (en-IN / co.in) - 100% Free."""
    try:
        # tld='co.in' selects Google's authentic Indian voice synthesizer
        tts = gTTS(text=text, lang="en", tld="co.in", slow=False)
        tts.save(output_path)
        print(f"[Voice Engine SUCCESS] Saved Indian voiceover to {output_path}")
        return output_path
    except Exception as e:
        print(f"[Voice Engine Fallback] gTTS Indian accent error: {e}")
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(output_path)
        return output_path

def generate_audio_elevenlabs_indian(text: str, output_path: str = "voiceover.mp3", voice_id: str = "IKne3meq5aSn9XLyUdCD") -> str:
    """Generates Indian male voiceover using ElevenLabs API when key is available."""
    api_key = config.ELEVENLABS_API_KEY or os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("[Voice Engine] ElevenLabs API key missing. Falling back to authentic Indian gTTS voice...")
        return generate_audio_gtts_indian(text, output_path)

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
        print(f"[Voice Engine SUCCESS] Saved ElevenLabs Indian voiceover to {output_path}")
        return output_path
    else:
        print(f"[Voice Engine Warning] ElevenLabs status {response.status_code}. Falling back to gTTS Indian voice...")
        return generate_audio_gtts_indian(text, output_path)

def create_voiceover(text: str, output_path: str = "voiceover.mp3") -> str:
    """Smart dispatcher for authentic Indian male voiceover creation."""
    if config.ELEVENLABS_API_KEY or os.environ.get("ELEVENLABS_API_KEY"):
        return generate_audio_elevenlabs_indian(text, output_path)
    return generate_audio_gtts_indian(text, output_path)

if __name__ == "__main__":
    test_text = "Bhai, agar tum 2026 mein bhi saara kaam manually kar rahe ho, toh tum 3 ghante waste kar rahe ho!"
    create_voiceover(test_text, "test_indian_voice.mp3")
