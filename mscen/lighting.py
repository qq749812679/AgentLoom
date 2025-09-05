from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
from PIL import Image

from .utils.colors import palette_for_theme


@dataclass
class LightFrame:
    r: int
    g: int
    b: int
    ms: int


def _clamp(x: int) -> int:
    return max(0, min(255, int(x)))


def generate_lighting_from_theme(theme: str) -> List[Dict[str, int]]:
    palette = palette_for_theme(theme)
    frames: List[Dict[str, int]] = []
    # simple 3-color slow breathing
    for rgb in palette:
        r, g, b = rgb
        for k in (0.3, 0.6, 1.0, 0.6, 0.3):
            frames.append({"r": _clamp(r * k), "g": _clamp(g * k), "b": _clamp(b * k), "ms": 500})
    return frames


def generate_lighting_from_image(img: Image.Image) -> List[Dict[str, int]]:
    small = img.resize((32, 32)).convert("RGB")
    arr = np.array(small)
    mean_rgb = arr.reshape(-1, 3).mean(axis=0)
    r, g, b = map(int, mean_rgb)
    frames: List[Dict[str, int]] = []
    for k in (0.2, 0.5, 1.0, 0.5, 0.2):
        frames.append({"r": _clamp(r * k), "g": _clamp(g * k), "b": _clamp(b * k), "ms": 600})
    return frames


def save_lighting_program(frames: List[Dict[str, int]], out_dir: Path, filename: str | None = None) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / (filename if filename else "lighting_program.json")
    with path.open("w", encoding="utf-8") as f:
        json.dump({"frames": frames}, f, ensure_ascii=False, indent=2)
    return path



