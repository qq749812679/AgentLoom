from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Tuple

import numpy as np
from scipy.io import wavfile


def _to_mono(audio: np.ndarray) -> np.ndarray:
    if audio.ndim == 1:
        return audio.astype(np.float32)
    # average stereo channels
    return audio.mean(axis=1).astype(np.float32)


def _normalize(audio: np.ndarray) -> np.ndarray:
    if audio.size == 0:
        return audio
    max_val = float(np.max(np.abs(audio)))
    if max_val < 1e-9:
        return np.zeros_like(audio)
    return audio / max_val


def _frame_signal(x: np.ndarray, win: int, hop: int) -> np.ndarray:
    if x.shape[0] < win:
        pad = np.zeros(win - x.shape[0], dtype=x.dtype)
        x = np.concatenate([x, pad], axis=0)
    num = 1 + (x.shape[0] - win) // hop
    frames = np.lib.stride_tricks.as_strided(
        x,
        shape=(num, win),
        strides=(x.strides[0] * hop, x.strides[0]),
        writeable=False,
    )
    return frames.copy()


def _spectral_centroid(frames: np.ndarray, sr: int) -> np.ndarray:
    window = np.hanning(frames.shape[1]).astype(frames.dtype)
    mags = np.abs(np.fft.rfft(frames * window, axis=1))
    freqs = np.fft.rfftfreq(frames.shape[1], d=1.0 / sr)
    denom = mags.sum(axis=1) + 1e-9
    sc = (mags * freqs).sum(axis=1) / denom
    return sc


def _energy(frames: np.ndarray) -> np.ndarray:
    return (frames ** 2).mean(axis=1)


def _percentile_scale(x: np.ndarray, p_low: float = 5, p_high: float = 95) -> np.ndarray:
    if x.size == 0:
        return x
    lo = np.percentile(x, p_low)
    hi = np.percentile(x, p_high)
    if hi - lo < 1e-9:
        return np.zeros_like(x)
    y = (x - lo) / (hi - lo)
    return np.clip(y, 0.0, 1.0)


def _hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
    h = h % 1.0
    i = int(h * 6.0)
    f = h * 6.0 - i
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)
    i = i % 6
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q
    return int(r * 255), int(g * 255), int(b * 255)


def generate_lighting_from_wav(wav_path: Path, win: int = 1024, hop: int = 512) -> List[Dict[str, int]]:
    sr, data = wavfile.read(wav_path)
    audio = _normalize(_to_mono(data))
    frames = _frame_signal(audio, win=win, hop=hop)
    ener = _percentile_scale(_energy(frames))
    cent = _percentile_scale(_spectral_centroid(frames, sr))

    # Map: centroid -> hue (blue 0.66 to red 0.0), energy -> value
    frames_list: List[Dict[str, int]] = []
    ms = int(hop / sr * 1000)
    for e, c in zip(ener, cent):
        hue = 0.66 * (1.0 - float(c))  # high centroid -> warm
        sat = 0.9
        val = 0.2 + 0.8 * float(e)
        r, g, b = _hsv_to_rgb(hue, sat, val)
        frames_list.append({"r": r, "g": g, "b": b, "ms": max(40, ms)})
    return frames_list



