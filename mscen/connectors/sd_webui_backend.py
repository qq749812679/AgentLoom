from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import Optional

import requests
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from ..core.cache import SimpleDiskCache
from ..core.logger import JsonlLogger


@dataclass
class SDWebUIParams:
    prompt: str
    negative_prompt: str = ""
    seed: Optional[int] = None
    steps: int = 28
    cfg_scale: float = 5.0
    width: int = 896
    height: int = 512
    sampler_name: str = "Euler a"


class SDWebUIBackend:
    def __init__(self, base_url: str, cache: SimpleDiskCache, logger: JsonlLogger) -> None:
        self.base_url = base_url.rstrip("/")
        self.cache = cache
        self.logger = logger

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8), reraise=True)
    def txt2img(self, params: SDWebUIParams) -> Image.Image:
        payload = {
            "prompt": params.prompt,
            "negative_prompt": params.negative_prompt,
            "seed": params.seed if params.seed is not None else -1,
            "steps": params.steps,
            "cfg_scale": params.cfg_scale,
            "width": params.width,
            "height": params.height,
            "sampler_name": params.sampler_name,
            "restore_faces": False,
            "batch_size": 1,
            "n_iter": 1,
        }
        cached = self.cache.exists("sdwebui_txt2img", payload)
        if cached:
            return Image.open(BytesIO(cached.read_bytes())).convert("RGB")

        self.logger.log({"event": "sdwebui.request", "payload": {k: v for k, v in payload.items() if k != "prompt"}})
        url = f"{self.base_url}/sdapi/v1/txt2img"
        resp = requests.post(url, json=payload, timeout=180)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("images"):
            raise RuntimeError("SD WebUI returned no images")
        import base64
        img_b64 = data["images"][0]
        img_bytes = base64.b64decode(img_b64.split(",")[-1])
        self.cache.write_bytes("sdwebui_txt2img", payload, img_bytes)
        self.logger.log({"event": "sdwebui.ok", "size": len(img_bytes)})
        return Image.open(BytesIO(img_bytes)).convert("RGB")


