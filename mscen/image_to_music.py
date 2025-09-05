from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
from PIL import Image

from .utils.audio import save_wav


SAMPLE_RATE = 22050


def _sine(freq: float, duration_s: float, amp: float = 0.2) -> np.ndarray:
    n = int(duration_s * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    return np.sin(2 * np.pi * freq * t) * amp


def _image_mood_params(img: Image.Image) -> Tuple[float, float]:
    small = img.resize((64, 64))
    arr = np.array(small).astype(np.float32)
    brightness = float(arr.mean() / 255.0)
    # crude contrast proxy
    contrast = float(arr.std() / 128.0)
    return brightness, contrast


def generate_music_from_image(img: Image.Image, duration_s: float, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    brightness, contrast = _image_mood_params(img)
    base_freq = 196 + int(196 * (1.0 - brightness))  # darker -> lower
    mod_freq = 2 + 6 * contrast

    n = int(duration_s * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    carrier = np.sin(2 * np.pi * base_freq * t)
    modulator = 0.5 * (1 + np.sin(2 * np.pi * mod_freq * t))
    audio = 0.2 * carrier * modulator

    out_path = out_dir / f"image_music_{abs(hash((int(brightness*1000), int(contrast*1000), duration_s))) % 10**8}.wav"
    return save_wav(audio, SAMPLE_RATE, out_path)



