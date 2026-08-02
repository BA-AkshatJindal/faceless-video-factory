import os
import math
import random
import httpx
from PIL import Image, ImageDraw, ImageFont
import config

try:
    from moviepy import ImageSequenceClip, AudioFileClip
except ImportError:
    from moviepy.editor import ImageSequenceClip, AudioFileClip

FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "Montserrat-Bold.ttf")
HOST_AVATAR_PATH = os.path.join(os.path.dirname(__file__), "assets", "indian_techie_host.png")

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

def get_indian_techie_host() -> Image.Image:
    """Loads the official Photorealistic Indian Tech Host Avatar."""
    if os.path.exists(HOST_AVATAR_PATH):
        try:
            return Image.open(HOST_AVATAR_PATH).convert("RGB")
        except Exception as e:
            print(f"[Video Engine] Error loading host avatar: {e}")
    return None

def fetch_cinematic_tool_broll(prompt_summary: str, output_path: str = "cinematic_broll.png", width: int = 720, height: int = 1280) -> str:
    """Fetch 4K Cinematic Dark Cyber-Tech B-Roll Graphic with Tool UI overlays from Pollinations.ai FLUX engine."""
    try:
        cinematic_prompt = f"4k cinematic dark mode tech studio workspace with blue and purple RGB ambient lighting, floating glassmorphism UI card of {prompt_summary}, sleek Mac coding desktop with particle HUD glow, professional video render".replace(" ", "%20")
        url = f"https://pollinations.ai/p/{cinematic_prompt}?width={width}&height={height}&model=flux-realism&seed={random.randint(1, 99999)}"
        res = httpx.get(url, timeout=10.0)
        if res.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(res.content)
            return output_path
    except Exception:
        pass
    return ""

def create_animated_frame(f_idx: int, total_frames: int, title: str, subtitle_text: str, host_img: Image.Image = None, broll_img: Image.Image = None, width: int = 720, height: int = 1280, output_path: str = "frame.png") -> str:
    """Generates a cinematic 9:16 vertical video frame featuring:
    - Photorealistic Indian Tech Host in studio setting.
    - Floating glassmorphism tool UI card overlays.
    - Animated blue & purple RGB ambient pulse rings.
    - Montserrat-Bold yellow/white typography.
    """
    if broll_img:
        img = broll_img.copy()
    else:
        img = Image.new("RGB", (width, height), color="#04060e")

    draw = ImageDraw.Draw(img)

    # 1. CINEMATIC RGB AMBIENT LIGHTING & DYNAMIC NEON PULSE RINGS
    pulse = math.sin(f_idx * 0.15) * 12
    radius1 = int(240 + pulse)
    radius2 = int(220 - pulse)

    center_x = width // 2
    center_y = 520

    # Draw glowing cyan & purple RGB ambient studio rings around host
    draw.ellipse([center_x - radius1, center_y - radius1, center_x + radius1, center_y + radius1], outline="#00e5ff", width=4)
    draw.ellipse([center_x - radius2, center_y - radius2, center_x + radius2, center_y + radius2], outline="#9d4edd", width=3)

    # 2. PASTE PHOTOREALISTIC INDIAN TECH HOST IN CENTER RING
    if host_img:
        try:
            avatar_resized = host_img.resize((380, 380))
            mask = Image.new("L", (380, 380), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([0, 0, 380, 380], fill=255)
            img.paste(avatar_resized, (center_x - 190, center_y - 190), mask)
        except Exception as e:
            print(f"[Video Engine] Paste note: {e}")

    # 3. TOP GLASSMORPHISM HEADER TITLE BADGE (Montserrat-Bold)
    font_header = get_font(36)
    font_subhead = get_font(18)

    box_top_y1 = 80
    box_top_y2 = 240
    draw.rounded_rectangle([30, box_top_y1, width - 30, box_top_y2], radius=18, fill=(10, 16, 32), outline="#00e5ff", width=4)

    words_title = (title[:36].upper() if title else "VIRAL TECH HACKS").split()
    if len(words_title) > 3:
        t_line1 = " ".join(words_title[:len(words_title)//2])
        t_line2 = " ".join(words_title[len(words_title)//2:])
        draw.text((center_x, box_top_y1 + 45), t_line1, fill="#ffffff", font=font_header, anchor="mm")
        draw.text((center_x, box_top_y1 + 95), t_line2, fill="#ffffff", font=font_header, anchor="mm")
        draw.text((center_x, box_top_y1 + 135), "⚡ REAL TECH CREATOR • CINEMATIC STUDIO", fill="#00e5ff", font=font_subhead, anchor="mm")
    else:
        draw.text((center_x, box_top_y1 + 55), title.upper(), fill="#ffffff", font=font_header, anchor="mm")
        draw.text((center_x, box_top_y1 + 120), "⚡ REAL TECH CREATOR • CINEMATIC STUDIO", fill="#00e5ff", font=font_subhead, anchor="mm")

    # 4. SUBTITLE OVERLAY (Big Bold Yellow Subtitles)
    font_sub = get_font(42)
    if subtitle_text:
        sub_box_y1 = 810
        sub_box_y2 = 1040
        draw.rounded_rectangle([25, sub_box_y1, width - 25, sub_box_y2], radius=22, fill=(4, 8, 18), outline="#ffe600", width=4)

        words = subtitle_text.split()
        if len(words) > 3:
            line1 = " ".join(words[:len(words)//2])
            line2 = " ".join(words[len(words)//2:])
            draw.text((center_x, sub_box_y1 + 60), line1.upper(), fill="#ffe600", font=font_sub, anchor="mm")
            draw.text((center_x, sub_box_y1 + 150), line2.upper(), fill="#ffffff", font=font_sub, anchor="mm")
        else:
            draw.text((center_x, (sub_box_y1 + sub_box_y2) // 2), subtitle_text.upper(), fill="#ffe600", font=font_sub, anchor="mm")

    img.save(output_path)
    return output_path

def render_short_video(voiceover_path: str, script_data: dict, output_path: str = "final_short.mp4") -> str:
    """Renders full 9:16 vertical video implementing the Cinematic Tech Studio Visual Prompt Blueprint."""
    print("[Video Engine] Starting Cinematic Tech Studio video compilation...")
    
    # 1. Load Audio Voiceover
    audio_clip = AudioFileClip(voiceover_path)
    duration = audio_clip.duration
    fps = 24

    # 2. Fetch Cinematic B-Roll Graphic
    broll_path = fetch_cinematic_tool_broll(script_data.get("title", "AI tool dashboard"))
    broll_img = None
    if broll_path and os.path.exists(broll_path):
        try:
            broll_img = Image.open(broll_path).convert("RGB").resize((720, 1280))
            dark_overlay = Image.new("RGB", (720, 1280), color="#000000")
            broll_img = Image.blend(broll_img, dark_overlay, alpha=0.65)
        except Exception:
            broll_img = None

    # 3. Load Photorealistic Indian Tech Host Avatar
    host_img = get_indian_techie_host()

    # 4. Split script into timed chunks
    words = script_data.get("voice_script", "").split()
    chunks = []
    chunk_size = 5
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))

    if not chunks:
        chunks = [script_data.get("title", "VIRAL TECH HACKS")]

    # 5. Create animated frame sequence
    title = script_data.get("title", "TECH HACKS")
    frame_files = []
    chunk_duration = duration / len(chunks)

    temp_dir = "temp_frames"
    os.makedirs(temp_dir, exist_ok=True)

    total_frames_count = int(duration * fps)
    print(f"[Video Engine] Rendering {total_frames_count} frames with Cinematic Studio aesthetics...")

    for f_idx in range(total_frames_count):
        t = f_idx / fps
        chunk_idx = min(int(t / chunk_duration), len(chunks) - 1)
        sub_text = chunks[chunk_idx]

        frame_path = os.path.join(temp_dir, f"frame_{f_idx:05d}.png")
        create_animated_frame(f_idx, total_frames_count, title, sub_text, host_img=host_img, broll_img=broll_img, output_path=frame_path)
        frame_files.append(frame_path)

    # 6. Create ImageSequenceClip from frames
    print("[Video Engine] Encoding Cinematic Studio MP4 video file...")
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

    # Clean up temporary frames & graphics
    try:
        if broll_path and os.path.exists(broll_path):
            os.remove(broll_path)
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)
    except Exception:
        pass

    print(f"[Video Engine SUCCESS] Rendered Cinematic Studio video to {output_path}")
    return output_path

if __name__ == "__main__":
    create_animated_frame(0, 30, "3 FREE AI TOOLS THAT FEEL ILLEGAL TO KNOW", "STOP WASTING HOURS DOING MANUAL WORK IN 2026", output_path="preview_cinematic.png")
