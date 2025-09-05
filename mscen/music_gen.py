from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np

from .utils.audio import save_wav, mix_tracks
from .utils.colors import palette_for_theme


SAMPLE_RATE = 22050


def _env(length: int, attack: int = 1000, release: int = 2000) -> np.ndarray:
    env = np.ones(length, dtype=np.float32)
    attack = max(1, min(attack, length))
    release = max(1, min(release, length))
    env[:attack] *= np.linspace(0.0, 1.0, attack, dtype=np.float32)
    env[-release:] *= np.linspace(1.0, 0.0, release, dtype=np.float32)
    return env


def _sine(freq: float, duration_s: float, amp: float = 0.2) -> np.ndarray:
    n = int(duration_s * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    wave = np.sin(2 * np.pi * freq * t) * amp
    return wave * _env(n)


def _pad_to(audio: np.ndarray, length: int) -> np.ndarray:
    if audio.shape[0] >= length:
        return audio[:length]
    out = np.zeros(length, dtype=np.float32)
    out[: audio.shape[0]] = audio
    return out


def _theme_to_scale(theme: str) -> Tuple[int, list[int]]:
    t = theme.lower()
    if "睡" in theme or "sleep" in t or "禅" in theme or "zen" in t:
        base = 261  # C4
        scale = [0, 3, 5, 7, 10, 12]
    elif "圣诞" in theme or "christmas" in t:
        base = 293  # D4
        scale = [0, 2, 4, 7, 9, 12]
    elif "雷" in theme or "thunder" in t:
        base = 196  # G3
        scale = [0, 1, 3, 6, 7, 10, 12]
    elif "派对" in theme or "party" in t:
        base = 329  # E4
        scale = [0, 2, 4, 7, 9, 12]
    else:
        base = 261
        scale = [0, 2, 5, 7, 9, 12]
    return base, scale


def _palette_tempo(theme: str) -> float:
    theme_l = theme.lower()
    if "睡" in theme or "sleep" in theme_l or "禅" in theme or "zen" in theme_l:
        return 60.0
    if "雷" in theme or "thunder" in theme_l:
        return 90.0
    if "派对" in theme or "party" in theme_l:
        return 120.0
    if "圣诞" in theme or "christmas" in theme_l:
        return 80.0
    return 90.0


def generate_music_from_theme(theme: str, duration_s: float, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    n = int(duration_s * SAMPLE_RATE)
    base, scale = _theme_to_scale(theme)
    bpm = _palette_tempo(theme)
    beat_s = 60.0 / bpm
    step_s = beat_s / 2.0

    times = np.arange(0.0, duration_s, step_s)
    layers = []
    for idx, t0 in enumerate(times):
        degree = scale[idx % len(scale)]
        freq = base * (2 ** (degree / 12.0))
        seg = _sine(freq, min(step_s * 1.9, duration_s - t0), amp=0.2)
        offset = int(t0 * SAMPLE_RATE)
        lay = np.zeros(n, dtype=np.float32)
        lay[offset : offset + seg.shape[0]] += seg
        layers.append(lay)

    # Simple bass drone from palette darkness
    palette = palette_for_theme(theme)
    mean_brightness = np.mean([r + g + b for (r, g, b) in palette]) / (255 * 3)
    bass_freq = 110 if mean_brightness < 0.5 else 147
    bass = _sine(bass_freq, duration_s, amp=0.12)
    bass = _pad_to(bass, n)
    mix = mix_tracks(tuple(layers + [bass]))

    out_path = out_dir / f"music_{abs(hash((theme, duration_s))) % 10**8}.wav"
    return save_wav(mix, SAMPLE_RATE, out_path)



