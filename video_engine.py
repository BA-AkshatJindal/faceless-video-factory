import os
import random
from PIL import Image, ImageDraw, ImageFont
import config

try:
    from moviepy import ImageSequenceClip, AudioFileClip
except ImportError:
    from moviepy.editor import ImageSequenceClip, AudioFileClip

def create_composed_frame(title: str, subtitle_text: str, width: int = 720, height: int = 1280, output_path: str = "frame.png") -> str:
    """Generates a complete pre-composited 9:16 vertical frame (Background + Subtitles) using Pillow.
    Pre-compositing avoids heavy RGBA float64 memory allocations in MoviePy.
    """
    img = Image.new("RGB", (width, height), color="#090d16")
    draw = ImageDraw.Draw(img)

    # Draw vertical subtle gradient / background accents
    for y in range(height):
        r = int(9 + (15 - 9) * (y / height))
        g = int(13 + (30 - 13) * (y / height))
        b = int(22 + (50 - 22) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Add decorative glow circles
    draw.ellipse([width//2 - 250, 100, width//2 + 250, 600], fill=(20, 45, 90))
    
    # Header badge
    draw.rectangle([50, 90, width - 50, 180], outline="#00e5ff", width=3)
    
    try:
        font_large = ImageFont.truetype("arial.ttf", 32)
        font_small = ImageFont.truetype("arial.ttf", 22)
        font_sub = ImageFont.truetype("arialbd.ttf", 36)
    except Exception:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Draw header text
    display_title = title[:30].upper() if title else "VIRAL TECH HACKS"
    draw.text((width // 2, 135), display_title, fill="#ffffff", font=font_large, anchor="mm")
    draw.text((width // 2, 215), "VIRAL TECH BREAKDOWN 2026", fill="#00e5ff", font=font_small, anchor="mm")

    # Draw Subtitle Pill Box & Text if present
    if subtitle_text:
        box_y1 = 750
        box_y2 = 880
        draw.rounded_rectangle([40, box_y1, width - 40, box_y2], radius=15, fill="#040914", outline="#00e5ff", width=2)
        draw.text((width // 2, (box_y1 + box_y2) // 2), subtitle_text, fill="#ffe600", font=font_sub, anchor="mm")

    img.save(output_path)
    return output_path

def render_short_video(voiceover_path: str, script_data: dict, output_path: str = "final_short.mp4") -> str:
    """Renders full 9:16 vertical video using lightweight pre-composited Pillow frames and MoviePy."""
    print("[Video Engine] Starting lightweight video compilation...")
    
    # 1. Load Audio Voiceover
    audio_clip = AudioFileClip(voiceover_path)
    duration = audio_clip.duration
    fps = 24  # 24 FPS for fast rendering and low RAM usage

    # 2. Split script into timed chunks
    words = script_data.get("voice_script", "").split()
    chunks = []
    chunk_size = 5
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))

    if not chunks:
        chunks = [script_data.get("title", "VIRAL TECH HACKS")]

    # 3. Create pre-composited frame images
    title = script_data.get("title", "TECH HACKS")
    frame_files = []
    chunk_duration = duration / len(chunks)

    temp_dir = "temp_frames"
    os.makedirs(temp_dir, exist_ok=True)

    print(f"[Video Engine] Generating {len(chunks)} pre-composited frames...")
    total_frames_count = int(duration * fps)

    for f_idx in range(total_frames_count):
        t = f_idx / fps
        chunk_idx = min(int(t / chunk_duration), len(chunks) - 1)
        sub_text = chunks[chunk_idx]

        frame_path = os.path.join(temp_dir, f"frame_{f_idx:05d}.png")
        if f_idx > 0 and chunk_idx == min(int((f_idx - 1) / fps / chunk_duration), len(chunks) - 1):
            frame_files.append(frame_files[-1])
        else:
            create_composed_frame(title, sub_text, output_path=frame_path)
            frame_files.append(frame_path)

    # 4. Create ImageSequenceClip from frames
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

    # Clean up temporary frame directory
    try:
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)
    except Exception:
        pass

    print(f"[Video Engine SUCCESS] Rendered final 9:16 vertical video to {output_path}")
    return output_path

if __name__ == "__main__":
    create_composed_frame("AI TOOLS HACK", "Sample subtitle text")
