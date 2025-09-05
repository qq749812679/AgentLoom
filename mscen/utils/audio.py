from pathlib import Path
from typing import Tuple

import numpy as np
from scipy.io import wavfile


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def normalize_to_int16(audio: np.ndarray) -> np.ndarray:
    if audio.size == 0:
        return np.zeros(0, dtype=np.int16)
    max_val = float(np.max(np.abs(audio)))
    if max_val < 1e-9:
        return np.zeros_like(audio, dtype=np.int16)
    scaled = audio / max_val
    return np.clip(scaled * 32767.0, -32768.0, 32767.0).astype(np.int16)


def save_wav(audio: np.ndarray, sample_rate: int, out_path: Path) -> Path:
    ensure_parent(out_path)
    data = normalize_to_int16(audio)
    wavfile.write(out_path, sample_rate, data)
    return out_path


def mix_tracks(tracks: Tuple[np.ndarray, ...]) -> np.ndarray:
    if not tracks:
        return np.array([], dtype=np.float32)
    max_len = max(track.shape[0] for track in tracks)
    mix = np.zeros(max_len, dtype=np.float32)
    for t in tracks:
        if t.shape[0] < max_len:
            padded = np.zeros(max_len, dtype=np.float32)
            padded[: t.shape[0]] = t.astype(np.float32)
            mix += padded
        else:
            mix += t[:max_len].astype(np.float32)
    mix /= max(1.0, float(len(tracks)))
    return mix



