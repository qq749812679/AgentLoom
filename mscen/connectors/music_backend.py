from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests

from ..core.cache import SimpleDiskCache
from ..core.logger import JsonlLogger


@dataclass
class MusicGenParams:
    prompt: str
    duration_s: float
    style: Optional[str] = None


class MusicBackend:
    def __init__(self, base_url: str, cache: SimpleDiskCache, logger: JsonlLogger) -> None:
        self.base_url = base_url.rstrip("/")
        self.cache = cache
        self.logger = logger

    def generate(self, params: MusicGenParams, out_path: Path) -> Path:
        payload = {
            "prompt": params.prompt,
            "duration": params.duration_s,
            "style": params.style,
        }
        cached = self.cache.exists("musicgen", payload)
        if cached:
            out_path.write_bytes(cached.read_bytes())
            return out_path

        self.logger.log({"event": "musicgen.request", "payload": payload})
        resp = requests.post(f"{self.base_url}/musicgen", json=payload, timeout=300)
        resp.raise_for_status()
        data = resp.content
        self.cache.write_bytes("musicgen", payload, data)
        self.logger.log({"event": "musicgen.ok", "size": len(data)})
        out_path.write_bytes(data)
        return out_path



