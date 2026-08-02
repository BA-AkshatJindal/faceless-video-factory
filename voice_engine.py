import os
import httpx
from gtts import gTTS
import config

def generate_audio_gtts(text: str, output_path: str = "voiceover.mp3", lang: str = "en") -> str:
    """Generates audio voiceover using Google Text-to-Speech (gTTS) - 100% Free."""
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_path)
    print(f"[Voice Engine] Saved gTTS voiceover to {output_path}")
    return output_path

def generate_audio_elevenlabs(text: str, output_path: str = "voiceover.mp3", voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> str:
    """Generates audio voiceover using ElevenLabs API (Requires ELEVENLABS_API_KEY)."""
    api_key = config.ELEVENLABS_API_KEY or os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("[Voice Engine] ElevenLabs API key missing. Falling back to gTTS...")
        return generate_audio_gtts(text, output_path)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }

    response = httpx.post(url, json=data, headers=headers, timeout=30.0)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"[Voice Engine] Saved ElevenLabs voiceover to {output_path}")
        return output_path
    else:
        print(f"[Voice Engine Error] ElevenLabs returned status {response.status_code}. Falling back to gTTS...")
        return generate_audio_gtts(text, output_path)

def create_voiceover(text: str, output_path: str = "voiceover.mp3") -> str:
    """Smart dispatcher for voiceover creation."""
    if config.ELEVENLABS_API_KEY or os.environ.get("ELEVENLABS_API_KEY"):
        return generate_audio_elevenlabs(text, output_path)
    return generate_audio_gtts(text, output_path)

if __name__ == "__main__":
    test_text = "Here are 3 secret AI tools that feel illegal to know in 2026. Tool number one is Perplexity."
    create_voiceover(test_text, "test_voice.mp3")
