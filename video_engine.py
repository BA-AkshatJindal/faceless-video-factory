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
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

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

def load_action_scene_assets() -> dict:
    """Loads 4 distinct permanent bundled action scene visual assets."""
    scenes = {}
    scene_files = {
        "host_talking": "indian_techie_host.png",
        "hands_typing": "hands_typing_code.png",
        "code_dashboard": "code_dashboard.png",
        "creator_gesturing": "creator_gesturing.png"
    }
    
    # Load fallback base image
    base_host_path = os.path.join(ASSETS_DIR, "indian_techie_host.png")
    base_host_img = None
    if os.path.exists(base_host_path):
        try:
            base_host_img = Image.open(base_host_path).convert("RGB")
        except Exception:
            base_host_img = None

    for key, filename in scene_files.items():
        path = os.path.join(ASSETS_DIR, filename)
        if os.path.exists(path):
            try:
                scenes[key] = Image.open(path).convert("RGB")
            except Exception:
                scenes[key] = base_host_img
        else:
            scenes[key] = base_host_img

    return scenes

def draw_text_with_outline(draw, position, text, font, fill_color="#FFFFFF", outline_color="#000000", outline_width=4, anchor="mm"):
    """Draws text with heavy dark outline/shadow for 100% readability over video background."""
    x, y = position
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill_color, anchor=anchor)

def create_action_cut_frame(f_idx: int, total_frames: int, title: str, subtitle_text: str, current_scene_img: Image.Image, width: int = 720, height: int = 1280, output_path: str = "frame.png") -> str:
    """Generates a 9:16 vertical frame with dynamic multi-camera action cuts and 52px Montserrat captions."""
    if current_scene_img:
        # Subtle motion zoom within scene cut
        scale = 1.0 + (math.sin(f_idx * 0.08) * 0.02)
        new_w = int(width * scale)
        new_h = int(height * scale)
        img_resized = current_scene_img.resize((new_w, new_h))
        crop_x = (new_w - width) // 2
        crop_y = (new_h - height) // 2
        img = img_resized.crop((crop_x, crop_y, crop_x + width, crop_y + height)).copy()
        
        dark_overlay = Image.new("RGB", (width, height), color="#000000")
        img = Image.blend(img, dark_overlay, alpha=0.30)
    else:
        img = Image.new("RGB", (width, height), color="#060913")

    draw = ImageDraw.Draw(img)
    center_x = width // 2

    # Sleek Top Header Badge
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
    """Renders full 9:16 vertical video featuring MULTI-SCENE ACTION CAMERA CUTS across 4 distinct visual assets."""
    print("[Video Engine] Starting Multi-Scene Action Camera Cut Video Compilation...")
    
    audio_clip = AudioFileClip(voiceover_path)
    duration = audio_clip.duration
    fps = 24

    # Load 4 distinct action scene visual assets
    scenes = load_action_scene_assets()

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
    print(f"[Video Engine] Animating {total_frames_count} frames with hard camera cuts every 6 seconds across 4 distinct action scenes...")

    # Action scene switching sequence across 60 seconds
    scene_sequence = ["host_talking", "hands_typing", "code_dashboard", "creator_gesturing"]

    for f_idx in range(total_frames_count):
        t = f_idx / fps
        chunk_idx = min(int(t / chunk_duration), len(chunks) - 1)
        sub_text = chunks[chunk_idx]

        # Switch action camera angle every 6 seconds
        scene_idx = int(t / 6.0) % len(scene_sequence)
        current_scene_name = scene_sequence[scene_idx]
        current_scene_img = scenes.get(current_scene_name) or scenes["host_talking"]

        frame_path = os.path.join(temp_dir, f"frame_{f_idx:05d}.png")
        create_action_cut_frame(f_idx, total_frames_count, title, sub_text, current_scene_img=current_scene_img, output_path=frame_path)
        frame_files.append(frame_path)

    print("[Video Engine] Encoding multi-scene action MP4 video file...")
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

    print(f"[Video Engine SUCCESS] Rendered multi-scene action video to {output_path}")
    return output_path

if __name__ == "__main__":
    test_img = Image.new("RGB", (720, 1280), color="#0a1020")
    create_action_cut_frame(0, 30, "3 FREE AI TOOLS THAT FEEL ILLEGAL TO KNOW", "STOP WASTING HOURS DOING MANUAL WORK IN 2026", current_scene_img=test_img, output_path="preview_action.png")
