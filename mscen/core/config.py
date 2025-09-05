from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass
class ModelEndpoints:
    image_txt2img_url: Optional[str] = None  # e.g. SDXL/Flux endpoint
    sdwebui_url: Optional[str] = None        # Stable Diffusion WebUI
    music_gen_url: Optional[str] = None      # e.g. MusicGen endpoint
    stt_url: Optional[str] = None            # e.g. Whisper server
    tts_url: Optional[str] = None            # e.g. Edge TTS proxy


@dataclass
class DeviceConfig:
    hue_bridge_ip: Optional[str] = None
    hue_username: Optional[str] = None
    wled_ip: Optional[str] = None


@dataclass
class Config:
    endpoints: ModelEndpoints
    devices: DeviceConfig
    outputs_dir: Path
    api_key: Optional[str] = None


def load_config(base_dir: Path) -> Config:
    env_path = base_dir / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    endpoints = ModelEndpoints(
        image_txt2img_url=os.getenv("IMAGE_TXT2IMG_URL") or os.getenv("IMAGE_GENERATION_URL") or None,
        sdwebui_url=os.getenv("SDWEBUI_URL") or None,
        music_gen_url=os.getenv("MUSIC_GEN_URL") or os.getenv("MUSIC_GENERATION_URL") or None,
        stt_url=os.getenv("STT_URL") or None,
        tts_url=os.getenv("TTS_URL") or None,
    )
    devices = DeviceConfig(
        hue_bridge_ip=os.getenv("HUE_BRIDGE_IP") or None,
        hue_username=os.getenv("HUE_USERNAME") or None,
        wled_ip=os.getenv("WLED_IP") or None,
    )
    outputs = base_dir / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    api_key = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY") or None
    return Config(endpoints=endpoints, devices=devices, outputs_dir=outputs, api_key=api_key)



