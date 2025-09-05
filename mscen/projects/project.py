from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any
import json

from ..lighting import generate_lighting_from_theme


@dataclass
class Room:
    name: str
    brightness: float = 1.0  # 0.0 ~ 1.0
    delay_ms: int = 0        # initial delay before frames start


@dataclass
class Project:
    name: str
    theme: str
    rooms: List[Room]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "theme": self.theme,
            "rooms": [asdict(r) for r in self.rooms],
        }


def _apply_brightness(frames: List[Dict[str, int]], brightness: float) -> List[Dict[str, int]]:
    b = max(0.0, min(1.0, float(brightness)))
    out: List[Dict[str, int]] = []
    for f in frames:
        out.append({
            "r": max(0, min(255, int(f["r"] * b))),
            "g": max(0, min(255, int(f["g"] * b))),
            "b": max(0, min(255, int(f["b"] * b))),
            "ms": int(f["ms"]),
        })
    return out


def compile_project(proj: Project) -> Dict[str, List[Dict[str, int]]]:
    base_frames = generate_lighting_from_theme(proj.theme)
    per_room: Dict[str, List[Dict[str, int]]] = {}
    for room in proj.rooms:
        frames = _apply_brightness(base_frames, room.brightness)
        if room.delay_ms > 0:
            # Insert an initial black frame to represent delay
            per_room[room.name] = [{"r": 0, "g": 0, "b": 0, "ms": int(room.delay_ms)}] + frames
        else:
            per_room[room.name] = frames
    return per_room


def save_project(proj: Project, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"project_{proj.name}.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(proj.to_dict(), f, ensure_ascii=False, indent=2)
    return path


