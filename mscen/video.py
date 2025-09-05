from __future__ import annotations

from pathlib import Path
from typing import Optional

from PIL import Image
from moviepy.editor import ImageClip, AudioFileClip


def compose_image_music_to_mp4(image_path: Path, audio_path: Path, out_path: Path, fps: int = 30) -> Path:
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    clip = ImageClip(str(image_path)).set_duration(AudioFileClip(str(audio_path)).duration)
    clip = clip.set_fps(fps)
    audio = AudioFileClip(str(audio_path))
    clip = clip.set_audio(audio)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    clip.write_videofile(str(out_path), codec="libx264", audio_codec="aac", fps=fps, verbose=False, logger=None)
    return out_path


