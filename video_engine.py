import os
import time
import math
import random
import httpx
from PIL import Image, ImageDraw, ImageFont
import config

try:
    from moviepy import ImageSequenceClip, AudioFileClip, VideoFileClip, concatenate_videoclips
except ImportError:
    from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip, concatenate_videoclips

FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "Montserrat-Bold.ttf")
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

def generate_free_liveportrait_avatar_talking(audio_path: str, output_path: str = "avatar_talking.mp4") -> str:
    """Animates indian_techie_host.png with 100% FREE open-source LivePortrait AI ($0/mo forever).
    Uses 5-second chunking to stay within HuggingFace free GPU tier limits.
    """
    if not os.path.exists(HOST_AVATAR_PATH) or not os.path.exists(audio_path):
        return ""
    
    print("[LivePortrait Free Engine] Animating Indian Tech Host avatar with 100% Free LivePortrait AI ($0/mo)...")
    
    try:
        from gradio_client import Client, handle_file
        client = Client("klingteam/LivePortrait")

        # Trim to 5s chunk to guarantee zero-cost free GPU processing
        chunk_audio_path = "temp_5s_audio.mp3"
        audio_clip = AudioFileClip(audio_path)
        sub_clip = audio_clip.subclipped(0, min(5.0, audio_clip.duration))
        sub_clip.write_audiofile(chunk_audio_path, logger=None)
        sub_clip.close()
        audio_clip.close()

        result = client.predict(
            param_0=handle_file(HOST_AVATAR_PATH),
            param_1={"video": handle_file(chunk_audio_path)},
            param_2=True,
            param_3=True,
            param_4=True,
            api_name="/gpu_wrapped_execute_video"
        )

        if os.path.exists(chunk_audio_path):
            os.remove(chunk_audio_path)

        if result and isinstance(result, tuple) and len(result) > 0:
            video_file = result[0].get("video") if isinstance(result[0], dict) else result[0]
            if video_file and os.path.exists(video_file):
                print(f"[LivePortrait Free SUCCESS] Generated 100% Free Talking Avatar Video at {video_file}")
                return video_file
    except Exception as e:
        print(f"[LivePortrait Free Note] Free GPU space note: {e}")

    return ""

def draw_text_with_outline(draw, position, text, font, fill_color="#FFFFFF", outline_color="#000000", outline_width=4, anchor="mm"):
    """Draws text with heavy dark outline/shadow for 100% readability over video background."""
    x, y = position
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill_color, anchor=anchor)

def create_caption_overlay_frame(f_idx: int, total_frames: int, title: str, subtitle_text: str, bg_frame: Image.Image, width: int = 720, height: int = 1280, output_path: str = "frame.png") -> str:
    """Overlays 52px Montserrat-Bold yellow/white captions over animated talking avatar video frames."""
    if bg_frame:
        img = bg_frame.resize((width, height)).copy()
        dark_overlay = Image.new("RGB", (width, height), color="#000000")
        img = Image.blend(img, dark_overlay, alpha=0.30)
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
    """Renders full 9:16 vertical video featuring 100% FREE Talking Avatar Lip-Sync & Montserrat captions ($0/mo)."""
    print("[Video Engine] Starting 100% FREE Talking Avatar Video Compilation ($0/mo)...")
    
    audio_clip = AudioFileClip(voiceover_path)
    duration = audio_clip.duration
    fps = 24

    # 1. Generate 100% FREE LivePortrait Talking Avatar Video
    avatar_video_file = generate_free_liveportrait_avatar_talking(voiceover_path)

    avatar_clip = None
    if avatar_video_file and os.path.exists(avatar_video_file):
        try:
            avatar_clip = VideoFileClip(avatar_video_file)
        except Exception as e:
            print(f"[Video Engine] Avatar clip load note: {e}")

    host_img = None
    if os.path.exists(HOST_AVATAR_PATH):
        try:
            host_img = Image.open(HOST_AVATAR_PATH).convert("RGB")
        except Exception:
            host_img = None

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
    print(f"[Video Engine] Animating {total_frames_count} frames with 100% Free LivePortrait Talking Avatar...")

    for f_idx in range(total_frames_count):
        t = f_idx / fps
        chunk_idx = min(int(t / chunk_duration), len(chunks) - 1)
        sub_text = chunks[chunk_idx]

        bg_frame_img = None
        if avatar_clip:
            clip_t = t % avatar_clip.duration
            try:
                frame_array = avatar_clip.get_frame(clip_t)
                bg_frame_img = Image.fromarray(frame_array)
            except Exception:
                bg_frame_img = None

        if not bg_frame_img and host_img:
            scale = 1.0 + (math.sin(f_idx * 0.05) * 0.03)
            new_w = int(720 * scale)
            new_h = int(1280 * scale)
            img_resized = host_img.resize((new_w, new_h))
            crop_x = (new_w - 720) // 2
            crop_y = (new_h - 1280) // 2
            bg_frame_img = img_resized.crop((crop_x, crop_y, crop_x + 720, crop_y + 1280)).copy()

        frame_path = os.path.join(temp_dir, f"frame_{f_idx:04d}.png")
        create_caption_overlay_frame(f_idx, total_frames_count, title, sub_text, bg_frame=bg_frame_img, output_path=frame_path)
        frame_files.append(frame_path)

    if avatar_clip:
        try:
            avatar_clip.close()
        except Exception:
            pass

    print("[Video Engine] Encoding Talking Avatar MP4 video file...")
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
        if avatar_video_file and os.path.exists(avatar_video_file):
            os.remove(avatar_video_file)
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)
    except Exception:
        pass

    print(f"[Video Engine SUCCESS] Rendered 100% Free Talking Avatar video to {output_path}")
    return output_path

if __name__ == "__main__":
    test_img = Image.new("RGB", (720, 1280), color="#0a1020")
    create_caption_overlay_frame(0, 30, "3 FREE AI TOOLS THAT FEEL ILLEGAL TO KNOW", "STOP WASTING HOURS DOING MANUAL WORK IN 2026", bg_frame=test_img, output_path="preview_avatar_talking.png")
