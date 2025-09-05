from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional

from PIL import Image

from ..core.logger import JsonlLogger
from ..core.cache import SimpleDiskCache
from ..image_gen import generate_scene_image
from ..music_gen import generate_music_from_theme
from ..image_to_music import generate_music_from_image
from ..lighting import generate_lighting_from_theme, generate_lighting_from_image, save_lighting_program


@dataclass
class OrchestratorConfig:
    outputs_dir: Path


class SafetyAgent:
    def __init__(self, logger: JsonlLogger) -> None:
        self.logger = logger

    def check_text(self, text: str) -> bool:
        banned = ["仇恨", "暴恐", "成人"]
        hit = any(k in text for k in banned)
        self.logger.log({"event": "safety.text", "hit": hit})
        return not hit


class MemoryAgent:
    def __init__(self) -> None:
        self.session: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self.session[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.session.get(key, default)


class Orchestrator:
    def __init__(self, cfg: OrchestratorConfig, logger: JsonlLogger, cache: SimpleDiskCache) -> None:
        self.cfg = cfg
        self.logger = logger
        self.cache = cache
        self.safety = SafetyAgent(logger)
        self.memory = MemoryAgent()

    def run_from_text(self, prompt: str, music_seconds: float = 20.0) -> Dict[str, Any]:
        if not self.safety.check_text(prompt):
            raise RuntimeError("文本不安全或不被允许")
        # image
        img = generate_scene_image(prompt, size=(896, 512))
        img_path = self.cfg.outputs_dir / "orch_scene.png"
        img.save(img_path)
        # music
        wav_path = generate_music_from_theme(prompt, duration_s=music_seconds, out_dir=self.cfg.outputs_dir)
        # lighting
        frames = generate_lighting_from_theme(prompt)
        prog_path = save_lighting_program(frames, self.cfg.outputs_dir, filename="orch_lighting.json")
        self.memory.set("last_prompt", prompt)
        return {"image": img_path, "music": wav_path, "lighting": prog_path}

    def run_from_image(self, img: Image.Image, music_seconds: float = 20.0) -> Dict[str, Any]:
        wav_path = generate_music_from_image(img, duration_s=music_seconds, out_dir=self.cfg.outputs_dir)
        frames = generate_lighting_from_image(img)
        prog_path = save_lighting_program(frames, self.cfg.outputs_dir, filename="orch_lighting_from_image.json")
        return {"music": wav_path, "lighting": prog_path}


