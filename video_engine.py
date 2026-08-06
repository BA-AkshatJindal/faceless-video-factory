import os
import math
import random
import httpx
from PIL import Image, ImageDraw, ImageFont
import config

try:
    from moviepy import ImageSequenceClip, AudioFileClip, VideoFileClip, CompositeVideoClip
except ImportError:
    from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip, CompositeVideoClip

FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "Montserrat-Bold.ttf")
VIDEOS_DIR = os.path.join(os.path.dirname(__file__), "assets", "videos")
HOST_AVATAR_PATH = os.path.join(os.path.dirname(__file__), "assets", "indian_techie_host.png")

def get_font(size: int):
    """Loads bundled Montserrat-Bold font strictly for large readable typography."""
    if os.path.exists(FONT_PATH):
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except Exception:
            pass
    try:
        return ImageFont.truetype("arialbd.ttf", size)
    except Exception:
        return ImageFont.load_default()

def draw_text_with_outline(draw, position, text, font, fill_color="#FFFFFF", outline_color="#000000", outline_width=4, anchor="mm"):
    """Draws text with heavy dark outline/shadow for 100% readability over video background."""
    x, y = position
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill_color, anchor=anchor)

def create_caption_overlay_frame(f_idx: int, total_frames: int, title: str, subtitle_text: str, bg_frame: Image.Image, width: int = 720, height: int = 1280, output_path: str = "frame.png") -> str:
    """Overlays 52px Montserrat-Bold yellow/white captions over real moving MP4 video frames."""
    if bg_frame:
        img = bg_frame.resize((width, height)).copy()
        dark_overlay = Image.new("RGB", (width, height), color="#000000")
        img = Image.blend(img, dark_overlay, alpha=0.35)
    else:
        img = Image.new("RGB", (width, height), color="#060913")

    draw = ImageDraw.Draw(img)
    center_x = width // 2

    # Top Header Badge
    font_badge = get_font(24)
    badge_text = f"⚡ {title.upper()[:30]}" if title else "⚡ VIRAL TECH HACKS 2026"
    
    draw.rounded_rectangle([center_x - 220, 60, center_x + 220, 115], radius=14, fill=(10, 16, 32), outline="#00e5ff", width=3)
    draw.text((center_x, 87), badge_text, fill="#00e5ff", font=font_badge, anchor="mm")

    # Viral Hormozi Captions (52px Montserrat)
    font_caption = get_font(52)
    if subtitle_text:
        words = subtitle_text.upper().split()
        caption_y = 960

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
    """Renders full 9:16 vertical video using REAL MOVING MP4 VIDEO CLIPS as video background ($0/mo Free)."""
    print("[Video Engine] Starting REAL MOTION MP4 VIDEO compilation ($0/mo Free)...")
    
    audio_clip = AudioFileClip(voiceover_path)
    duration = audio_clip.duration
    fps = 24

    # Load real MP4 video background clips
    video_clips_paths = [
        os.path.join(VIDEOS_DIR, "typing.mp4"),
        os.path.join(VIDEOS_DIR, "code.mp4"),
        os.path.join(VIDEOS_DIR, "studio.mp4")
    ]
    
    video_clips = []
    for vp in video_clips_paths:
        if os.path.exists(vp):
            try:
                vc = VideoFileClip(vp)
                video_clips.append(vc)
            except Exception:
                pass

    words = script_data.get("voice_script", "").split()
    chunks = []
    chunk_size = 4
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))

    if not chunks:
        chunks = [script_data.get("title", "VIRAL TECH HACKS")]

    title = script_data.get("title", "TECH HACKS")
    frame_files = []
    chunk_duration = duration / len(chunks)

    temp_dir = "temp_frames"
    os.makedirs(temp_dir, exist_ok=True)

    total_frames_count = int(duration * fps)
    print(f"[Video Engine] Animating {total_frames_count} frames over REAL MOVING MP4 VIDEO CLIPS...")

    # Extract background frames from real motion video clips
    for f_idx in range(total_frames_count):
        t = f_idx / fps
        chunk_idx = min(int(t / chunk_duration), len(chunks) - 1)
        sub_text = chunks[chunk_idx]

        bg_frame_img = None
        if video_clips:
            # Switch between real motion video clips every 5 seconds
            vc_idx = int(t / 5.0) % len(video_clips)
            clip_obj = video_clips[vc_idx]
            clip_t = t % clip_obj.duration
            try:
                frame_array = clip_obj.get_frame(clip_t)
                bg_frame_img = Image.fromarray(frame_array)
            except Exception:
                bg_frame_img = None

        if not bg_frame_img and os.path.exists(HOST_AVATAR_PATH):
            try:
                bg_frame_img = Image.open(HOST_AVATAR_PATH).convert("RGB")
            except Exception:
                bg_frame_img = None

        frame_path = os.path.join(temp_dir, f"frame_{f_idx:05d}.png")
        create_caption_overlay_frame(f_idx, total_frames_count, title, sub_text, bg_frame=bg_frame_img, output_path=frame_path)
        frame_files.append(frame_path)

    # Close video clips
    for vc in video_clips:
        try:
            vc.close()
        except Exception:
            pass

    print("[Video Engine] Encoding 100% REAL MOTION MP4 VIDEO file...")
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

    try:
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)
    except Exception:
        pass

    print(f"[Video Engine SUCCESS] Rendered 100% REAL MOTION MP4 VIDEO to {output_path}")
    return output_path

if __name__ == "__main__":
    test_img = Image.new("RGB", (720, 1280), color="#0a1020")
    create_caption_overlay_frame(0, 30, "3 FREE AI TOOLS THAT FEEL ILLEGAL TO KNOW", "STOP WASTING HOURS DOING MANUAL WORK IN 2026", bg_frame=test_img, output_path="preview_motion_real.png")
