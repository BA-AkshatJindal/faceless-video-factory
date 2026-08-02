import os
import random
import httpx
from PIL import Image, ImageDraw, ImageFont
import config

try:
    from moviepy import ImageSequenceClip, AudioFileClip
except ImportError:
    from moviepy.editor import ImageSequenceClip, AudioFileClip

FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "Montserrat-Bold.ttf")

def get_font(size: int):
    """Loads bundled Montserrat-Bold font or falls back safely."""
    if os.path.exists(FONT_PATH):
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except Exception:
            pass
    try:
        return ImageFont.truetype("arialbd.ttf", size)
    except Exception:
        return ImageFont.load_default()

def fetch_background_graphic(prompt_summary: str, output_path: str = "bg_art.png", width: int = 720, height: int = 1280) -> str:
    """Fetch high-quality AI background graphic from Pollinations.ai (Free) or fallback to procedural dark gradient."""
    try:
        encoded_prompt = prompt_summary.replace(" ", "%20")
        url = f"https://pollinations.ai/p/{encoded_prompt}?width={width}&height={height}&model=flux-realism&seed={random.randint(1, 99999)}"
        res = httpx.get(url, timeout=12.0)
        if res.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(res.content)
            return output_path
    except Exception as e:
        print(f"[Video Engine] Graphic fetch note: {e}")
    return ""

def create_composed_frame(title: str, subtitle_text: str, bg_image_path: str = "", width: int = 720, height: int = 1280, output_path: str = "frame.png") -> str:
    """Generates a high-impact pre-composited 9:16 vertical video frame.
    Features large readable typography, vibrant glow badges, and optimal safe zones for Shorts UI.
    """
    if bg_image_path and os.path.exists(bg_image_path):
        try:
            img = Image.open(bg_image_path).convert("RGB").resize((width, height))
            dark_overlay = Image.new("RGB", (width, height), color="#000000")
            img = Image.blend(img, dark_overlay, alpha=0.60)
        except Exception:
            img = Image.new("RGB", (width, height), color="#060913")
    else:
        img = Image.new("RGB", (width, height), color="#060913")

    draw = ImageDraw.Draw(img)

    # Ambient neon glow rings
    draw.ellipse([width//2 - 280, 260, width//2 + 280, 740], outline="#00e5ff", width=3)
    draw.ellipse([width//2 - 260, 280, width//2 + 260, 720], outline="#7b2cbf", width=2)

    # 1. TOP HEADER TITLE BADGE
    font_header = get_font(38)
    font_subhead = get_font(20)

    box_top_y1 = 100
    box_top_y2 = 270
    draw.rounded_rectangle([30, box_top_y1, width - 30, box_top_y2], radius=18, fill=(10, 16, 32), outline="#00e5ff", width=4)

    # Wrap title into 2 lines if needed
    words_title = (title[:40].upper() if title else "VIRAL TECH HACKS").split()
    if len(words_title) > 3:
        t_line1 = " ".join(words_title[:len(words_title)//2])
        t_line2 = " ".join(words_title[len(words_title)//2:])
        draw.text((width // 2, box_top_y1 + 50), t_line1, fill="#ffffff", font=font_header, anchor="mm")
        draw.text((width // 2, box_top_y1 + 100), t_line2, fill="#ffffff", font=font_header, anchor="mm")
        draw.text((width // 2, box_top_y1 + 145), "DAILY AI BREAKDOWN 2026", fill="#00e5ff", font=font_subhead, anchor="mm")
    else:
        draw.text((width // 2, box_top_y1 + 65), title.upper(), fill="#ffffff", font=font_header, anchor="mm")
        draw.text((width // 2, box_top_y1 + 130), "DAILY AI BREAKDOWN 2026", fill="#00e5ff", font=font_subhead, anchor="mm")

    # 2. SUBTITLE OVERLAY (Big Bold Yellow Subtitles)
    font_sub = get_font(44)
    if subtitle_text:
        sub_box_y1 = 800
        sub_box_y2 = 1030
        draw.rounded_rectangle([25, sub_box_y1, width - 25, sub_box_y2], radius=22, fill=(4, 8, 18), outline="#ffe600", width=4)

        words = subtitle_text.split()
        if len(words) > 3:
            line1 = " ".join(words[:len(words)//2])
            line2 = " ".join(words[len(words)//2:])
            draw.text((width // 2, sub_box_y1 + 60), line1.upper(), fill="#ffe600", font=font_sub, anchor="mm")
            draw.text((width // 2, sub_box_y1 + 150), line2.upper(), fill="#ffffff", font=font_sub, anchor="mm")
        else:
            draw.text((width // 2, (sub_box_y1 + sub_box_y2) // 2), subtitle_text.upper(), fill="#ffe600", font=font_sub, anchor="mm")

    img.save(output_path)
    return output_path

def render_short_video(voiceover_path: str, script_data: dict, output_path: str = "final_short.mp4") -> str:
    """Renders full 9:16 vertical video using lightweight pre-composited Pillow frames and MoviePy."""
    print("[Video Engine] Starting high-contrast video compilation...")
    
    # 1. Load Audio Voiceover
    audio_clip = AudioFileClip(voiceover_path)
    duration = audio_clip.duration
    fps = 24

    # 2. Fetch AI visual background graphic
    bg_art_path = fetch_background_graphic(script_data.get("title", "futuristic AI technology"))

    # 3. Split script into timed chunks
    words = script_data.get("voice_script", "").split()
    chunks = []
    chunk_size = 5
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))

    if not chunks:
        chunks = [script_data.get("title", "VIRAL TECH HACKS")]

    # 4. Create pre-composited frame images
    title = script_data.get("title", "TECH HACKS")
    frame_files = []
    chunk_duration = duration / len(chunks)

    temp_dir = "temp_frames"
    os.makedirs(temp_dir, exist_ok=True)

    print(f"[Video Engine] Generating {len(chunks)} pre-composited frames with Montserrat-Bold typography...")
    total_frames_count = int(duration * fps)

    for f_idx in range(total_frames_count):
        t = f_idx / fps
        chunk_idx = min(int(t / chunk_duration), len(chunks) - 1)
        sub_text = chunks[chunk_idx]

        frame_path = os.path.join(temp_dir, f"frame_{f_idx:05d}.png")
        if f_idx > 0 and chunk_idx == min(int((f_idx - 1) / fps / chunk_duration), len(chunks) - 1):
            frame_files.append(frame_files[-1])
        else:
            create_composed_frame(title, sub_text, bg_image_path=bg_art_path, output_path=frame_path)
            frame_files.append(frame_path)

    # 5. Create ImageSequenceClip from frames
    print("[Video Engine] Encoding MP4 video file...")
    clip = ImageSequenceClip(frame_files, fps=fps)
    
    if hasattr(clip, 'with_audio'):
        final_clip = clip.with_audio(audio_clip)
    else:
        final_clip = clip.set_audio(audio_clip)

    final_clip.write_videofile(
        output_path,
        fps=fps,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        logger=None
    )

    # Clean up temporary frames & art
    try:
        if bg_art_path and os.path.exists(bg_art_path):
            os.remove(bg_art_path)
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)
    except Exception:
        pass

    print(f"[Video Engine SUCCESS] Rendered final 9:16 vertical video to {output_path}")
    return output_path

if __name__ == "__main__":
    create_composed_frame("3 FREE AI TOOLS THAT FEEL ILLEGAL TO KNOW", "STOP WASTING HOURS DOING MANUAL WORK IN 2026", output_path="preview_frame.png")
