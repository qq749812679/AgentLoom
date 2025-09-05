from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any
import json


def frames_to_wled_preset(frames: List[Dict[str, int]]) -> Dict[str, Any]:
    # 简化的 WLED 状态序列，逐帧设置颜色与过渡时间（tt）
    sequence = []
    for f in frames:
        r, g, b, ms = f["r"], f["g"], f["b"], f["ms"]
        state = {
            "on": True,
            "bri": max(1, int(0.3 * 255 + 0.7 * max(r, g, b))),
            "tt": int(ms),
            "seg": [{"id": 0, "col": [[r, g, b]]}],
        }
        sequence.append(state)
    return {"sequence": sequence}


def save_wled_preset(frames: List[Dict[str, int]], out_dir: Path, filename: str = "wled_preset.json") -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename
    data = frames_to_wled_preset(frames)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


