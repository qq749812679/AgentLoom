from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Optional

import requests

from ..core.cache import SimpleDiskCache
from ..core.logger import JsonlLogger


@dataclass
class STTParams:
    language: Optional[str] = None  # e.g. 'zh', 'en'


class VoiceBackend:
    def __init__(self, stt_url: Optional[str], tts_url: Optional[str], cache: SimpleDiskCache, logger: JsonlLogger) -> None:
        self.stt_url = stt_url.rstrip("/") if stt_url else None
        self.tts_url = tts_url.rstrip("/") if tts_url else None
        self.cache = cache
        self.logger = logger

    def stt(self, wav_bytes: bytes, params: STTParams) -> str:
        if not self.stt_url:
            raise RuntimeError("STT endpoint not configured")
        payload = {"language": params.language}
        self.logger.log({"event": "stt.request", "payload": payload})
        files = {"file": ("audio.wav", wav_bytes, "audio/wav")}
        resp = requests.post(f"{self.stt_url}/stt", data=payload, files=files, timeout=120)
        resp.raise_for_status()
        text = resp.json().get("text", "")
        self.logger.log({"event": "stt.ok", "len": len(text)})
        return text

    def tts(self, text: str, voice: Optional[str], out_path: Path) -> Path:
        self.logger.log({"event": "tts.request", "payload": {"voice": voice, "chars": len(text)}})
        if self.tts_url:
            payload = {"text": text, "voice": voice}
            resp = requests.post(f"{self.tts_url}/tts", json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.content
            out_path.write_bytes(data)
            self.logger.log({"event": "tts.ok.remote", "size": len(data)})
            return out_path
        # fallback: edge-tts (mp3 output)
        try:
            import asyncio
            import edge_tts

            async def run_tts() -> bytes:
                communicate = edge_tts.Communicate(text, voice or "zh-CN-XiaoxiaoNeural")
                chunks = []
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        chunks.append(chunk["data"])  # bytes
                return b"".join(chunks)

            data = asyncio.run(run_tts())
            out_path.write_bytes(data)
            self.logger.log({"event": "tts.ok.edge", "size": len(data)})
            return out_path
        except Exception as e:
            raise RuntimeError(f"TTS failed: {e}")




