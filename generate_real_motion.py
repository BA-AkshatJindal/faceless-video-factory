import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def generate_procedural_motion_video(output_mp4_path: str, duration_sec: int = 15, fps: int = 24, width: int = 720, height: int = 1280):
    """Generates a high-quality 100% REAL MOTION MP4 video background featuring matrix digital code rain & floating particle waves."""
    try:
        from moviepy import ImageSequenceClip
    except ImportError:
        from moviepy.editor import ImageSequenceClip

    print(f"[Motion Generator] Creating 100% REAL MOTION MP4 video ({duration_sec}s @ {fps}fps)...")
    total_frames = duration_sec * fps
    temp_dir = "temp_motion_build"
    os.makedirs(temp_dir, exist_ok=True)

    # Matrix code columns setup
    num_cols = 20
    col_width = width // num_cols
    col_speeds = [random.randint(12, 25) for _ in range(num_cols)]
    col_y = [random.randint(-height, 0) for _ in range(num_cols)]
    chars = "0101010101010101010101010101010101010101"

    frame_paths = []
    for f in range(total_frames):
        img = Image.new("RGB", (width, height), color="#040714")
        draw = ImageDraw.Draw(img)

        # 1. Floating RGB Particle Wave Animation
        t = f / fps
        for i in range(15):
            px = int((width / 2) + math.sin(t * 2 + i) * 220)
            py = int((height / 2) + math.cos(t * 1.5 + i * 0.5) * 350)
            r = int(12 + math.sin(t * 3 + i) * 6)
            color = "#00e5ff" if i % 2 == 0 else "#9d4edd"
            draw.ellipse([px - r, py - r, px + r, py + r], outline=color, width=2)

        # 2. Dynamic Matrix Code Rain Motion
        for c in range(num_cols):
            x = c * col_width + 10
            col_y[c] += col_speeds[c]
            if col_y[c] > height:
                col_y[c] = -200

            y = col_y[c]
            for ch_idx, char in enumerate(chars[:15]):
                cy = y + (ch_idx * 25)
                if 0 <= cy < height:
                    alpha_color = "#00e5ff" if ch_idx == 0 else "#005577"
                    draw.text((x, cy), char, fill=alpha_color)

        frame_file = os.path.join(temp_dir, f"mframe_{f:04d}.png")
        img.save(frame_file)
        frame_paths.append(frame_file)

    clip = ImageSequenceClip(frame_paths, fps=fps)
    clip.write_videofile(output_mp4_path, fps=fps, codec="libx264", preset="ultrafast", logger=None)
    clip.close()

    # Clean up temp build frames
    for fp in frame_paths:
        try:
            os.remove(fp)
        except Exception:
            pass
    try:
        os.rmdir(temp_dir)
    except Exception:
        pass

    print(f"[Motion Generator SUCCESS] Saved REAL MOTION MP4 background to {output_mp4_path}")
    return output_mp4_path

if __name__ == "__main__":
    os.makedirs("assets/videos", exist_ok=True)
    generate_procedural_motion_video("assets/videos/tech_motion_bg.mp4")
