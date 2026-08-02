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
HOST_AVATAR_PATH = os.path.join(os.path.dirname(__file__), "assets", "indian_techie_host.png")

def get_font(size: int):
    """Loads bundled Montserrat-Bold font strictly to guarantee large readable typography."""
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

def draw_text_with_outline(draw, position, text, font, fill_color="#FFFFFF", outline_color="#000000", outline_width=4, anchor="mm"):
    """Draws text with heavy dark outline/shadow for 100% readability over video background."""
    x, y = position
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill_color, anchor=anchor)

def create_viral_short_frame(f_idx: int, total_frames: int, title: str, subtitle_text: str, host_img: Image.Image = None, width: int = 720, height: int = 1280, output_path: str = "frame.png") -> str:
    """Generates a 100% full-screen 9:16 vertical video frame:
    - Full-screen 9:16 Studio Host background (NO CIRCLE, NO CUTOUT, NO BOXES).
    - Ultra-large 52px Montserrat-Bold yellow/white captions overlaid directly on lower third.
    - Compact top header badge.
    """
    # 1. FULL-SCREEN 9:16 BACKGROUND (NO CIRCLE, NO CUTOUT)
    if host_img:
        img = host_img.resize((width, height)).copy()
        # Apply subtle dark vignette overlay so captions pop cleanly
        dark_overlay = Image.new("RGB", (width, height), color="#000000")
        img = Image.blend(img, dark_overlay, alpha=0.30)
    else:
        img = Image.new("RGB", (width, height), color="#060913")

    draw = ImageDraw.Draw(img)
    center_x = width // 2

    # 2. TOP HEADER BADGE (Compact & Clean)
    font_badge = get_font(24)
    badge_text = f"⚡ {title.upper()[:30]}" if title else "⚡ VIRAL TECH HACKS 2026"
    
    draw.rounded_rectangle([center_x - 220, 60, center_x + 220, 115], radius=14, fill=(10, 16, 32), outline="#00e5ff", width=3)
    draw.text((center_x, 87), badge_text, fill="#00e5ff", font=font_badge, anchor="mm")

    # 3. VIRAL ALEX HORMOZI STYLE CAPTIONS (Direct Overlay, Large 52px, NO BOXES)
    font_caption = get_font(52)
    if subtitle_text:
        words = subtitle_text.upper().split()
        caption_y = 960  # Positioned in lower third above YouTube Shorts UI buttons

        if len(words) > 3:
            line1 = " ".join(words[:len(words)//2])
            line2 = " ".join(words[len(words)//2:])
            draw_text_with_outline(draw, (center_x, caption_y - 35), line1, font_caption, fill_color="#FFE600", outline_color="#000000", outline_width=4)
            draw_text_with_outline(draw, (center_x, caption_y + 40), line2, font_caption, fill_color="#FFFFFF", outline_color="#000000", outline_width=4)
        else:
            draw_text_with_outline(draw, (center_x, caption_y), subtitle_text.upper(), font_caption, fill_color="#FFE600", outline_color="#000000", outline_width=4)

    img.save(output_path)
    return output_path

def render_short_video(voiceover_path: str, script_data: dict, output_path: str = "final_short.mp4") -> str:
    """Renders full 9:16 vertical video with 100% full-screen studio background (NO CIRCLE, NO BOXES)."""
    print("[Video Engine] Starting 100% full-screen 9:16 video compilation...")
    
    # 1. Load Audio Voiceover
    audio_clip = AudioFileClip(voiceover_path)
    duration = audio_clip.duration
    fps = 24

    # 2. Load Photorealistic Indian Tech Host Avatar
    host_img = get_indian_techie_host()

    # 3. Split script into timed chunks
    words = script_data.get("voice_script", "").split()
    chunks = []
    chunk_size = 4
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))

    if not chunks:
        chunks = [script_data.get("title", "VIRAL TECH HACKS")]

    # 4. Create animated frame sequence
    title = script_data.get("title", "TECH HACKS")
    frame_files = []
    chunk_duration = duration / len(chunks)

    temp_dir = "temp_frames"
    os.makedirs(temp_dir, exist_ok=True)

    total_frames_count = int(duration * fps)
    print(f"[Video Engine] Rendering {total_frames_count} frames with 100% full-screen 9:16 background (NO CIRCLE)...")

    for f_idx in range(total_frames_count):
        t = f_idx / fps
        chunk_idx = min(int(t / chunk_duration), len(chunks) - 1)
        sub_text = chunks[chunk_idx]

        frame_path = os.path.join(temp_dir, f"frame_{f_idx:05d}.png")
        create_viral_short_frame(f_idx, total_frames_count, title, sub_text, host_img=host_img, output_path=frame_path)
        frame_files.append(frame_path)

    # 5. Create ImageSequenceClip from frames
    print("[Video Engine] Encoding 100% full-screen MP4 video file...")
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

    # Clean up temporary frames
    try:
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)
    except Exception:
        pass

    print(f"[Video Engine SUCCESS] Rendered 100% full-screen video to {output_path}")
    return output_path

if __name__ == "__main__":
    create_viral_short_frame(0, 30, "3 FREE AI TOOLS THAT FEEL ILLEGAL TO KNOW", "STOP WASTING HOURS DOING MANUAL WORK IN 2026", output_path="preview_nocircle.png")
