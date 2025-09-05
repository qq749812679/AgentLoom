from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Optional

import requests
from PIL import Image

from ..core.cache import SimpleDiskCache
from ..core.logger import JsonlLogger


@dataclass
class Txt2ImgParams:
    prompt: str
    seed: Optional[int] = None
    width: int = 896
    height: int = 512
    guidance: float = 5.0


class ImageBackend:
    def __init__(self, base_url: str, cache: SimpleDiskCache, logger: JsonlLogger) -> None:
        self.base_url = base_url.rstrip("/")
        self.cache = cache
        self.logger = logger

    def txt2img(self, params: Txt2ImgParams) -> Image.Image:
        payload = {
            "prompt": params.prompt,
            "seed": params.seed,
            "width": params.width,
            "height": params.height,
            "guidance": params.guidance,
        }
        cached = self.cache.exists("txt2img", payload)
        if cached:
            return Image.open(BytesIO(cached.read_bytes())).convert("RGB")

        self.logger.log({"event": "txt2img.request", "payload": payload})
        resp = requests.post(f"{self.base_url}/txt2img", json=payload, timeout=120)
        resp.raise_for_status()
        img_bytes = resp.content
        self.cache.write_bytes("txt2img", payload, img_bytes)
        self.logger.log({"event": "txt2img.ok", "size": len(img_bytes)})
        return Image.open(BytesIO(img_bytes)).convert("RGB")



