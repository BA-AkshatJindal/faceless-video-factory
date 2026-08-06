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

def fetch_action_scene_graphic(scene_type: str, output_path: str, width: int = 720, height: int = 1280) -> str:
    """Fetch distinct 4K action scene graphics (typing code, multi-monitor dashboards, creator gesturing)."""
    try:
        scene_prompts = {
            "host_talking": "4k studio portrait of handsome young indian male tech founder developer talking to camera in dark mode workspace with blue and purple rgb ambient lighting",
            "hands_typing": "cinematic close up shot of hands typing code fast on mechanical keyboard with glowing rgb backlit keys and multiple coding monitors in dark studio",
            "code_dashboard": "over the shoulder shot of multiple glowing 4k monitors displaying python code editor terminal windows and ai tool dashboards",
            "creator_gesturing": "medium shot of young indian tech developer smiling gesturing with hands in dark tech workspace with cyan neon backlighting"
        }
        prompt = scene_prompts.get(scene_type, scene_prompts["host_talking"])
        encoded_prompt = prompt.replace(" ", "%20")
        url = f"https://pollinations.ai/p/{encoded_prompt}?width={width}&height={height}&model=flux-realism&seed={random.randint(1, 99999)}"
        res = httpx.get(url, timeout=10.0)
        if res.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(res.content)
            return output_path
    except Exception as e:
        print(f"[Video Engine] Action scene fetch note: {e}")
    return ""

def draw_text_with_outline(draw, position, text, font, fill_color="#FFFFFF", outline_color="#000000", outline_width=4, anchor="mm"):
    """Draws text with heavy dark outline/shadow for 100% readability over video background."""
    x, y = position
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill_color, anchor=anchor)

def create_action_cut_frame(f_idx: int, total_frames: int, title: str, subtitle_text: str, current_scene_img: Image.Image, width: int = 720, height: int = 1280, output_path: str = "frame.png") -> str:
    """Generates a 9:16 vertical frame with dynamic action camera cuts, zoom motion, and 52px Montserrat captions."""
    if current_scene_img:
        scale = 1.0 + (math.sin(f_idx * 0.08) * 0.03)  # Smooth motion zoom
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
    """Renders full 9:16 vertical video featuring MULTI-SCENE ACTION CUTS (host talking, hands typing code, multi-monitors, gesturing)."""
    print("[Video Engine] Starting Multi-Scene Action Video Compilation...")
    
    audio_clip = AudioFileClip(voiceover_path)
    duration = audio_clip.duration
    fps = 24

    # Pre-generate / load 4 distinct action scene graphics
    temp_dir = "temp_frames"
    os.makedirs(temp_dir, exist_ok=True)

    print("[Video Engine] Fetching 4 distinct action scene visual assets...")
    scenes = {
        "host_talking": None,
        "hands_typing": None,
        "code_dashboard": None,
        "creator_gesturing": None
    }

    # Load primary host avatar
    if os.path.exists(HOST_AVATAR_PATH):
        try:
            scenes["host_talking"] = Image.open(HOST_AVATAR_PATH).convert("RGB")
        except Exception:
            pass

    # Fetch action shots
    for s_name in ["hands_typing", "code_dashboard", "creator_gesturing"]:
        path = fetch_action_scene_graphic(s_name, os.path.join(temp_dir, f"{s_name}.png"))
        if path and os.path.exists(path):
            try:
                scenes[s_name] = Image.open(path).convert("RGB")
            except Exception:
                scenes[s_name] = scenes["host_talking"]

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

    total_frames_count = int(duration * fps)
    print(f"[Video Engine] Animating {total_frames_count} frames with dynamic action cuts every 6-8 seconds...")

    # Action scene switching schedule across 60 seconds
    scene_sequence = ["host_talking", "hands_typing", "code_dashboard", "creator_gesturing"]

    for f_idx in range(total_frames_count):
        t = f_idx / fps
        chunk_idx = min(int(t / chunk_duration), len(chunks) - 1)
        sub_text = chunks[chunk_idx]

        # Switch action scene every 7 seconds
        scene_idx = int(t / 7.0) % len(scene_sequence)
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
