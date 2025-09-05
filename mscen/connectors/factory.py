from __future__ import annotations

from ..core.cache import SimpleDiskCache
from ..core.logger import JsonlLogger
from .image_backend import ImageBackend
from .sd_webui_backend import SDWebUIBackend
from .music_backend import MusicBackend
from .voice_backend import VoiceBackend


def build_image_backend(http_url: str | None, sdwebui_url: str | None, cache: SimpleDiskCache, logger: JsonlLogger):
    sd = SDWebUIBackend(sdwebui_url, cache, logger) if sdwebui_url else None
    http = ImageBackend(http_url, cache, logger) if http_url else None
    return sd, http


def build_music_backend(http_url: str | None, cache: SimpleDiskCache, logger: JsonlLogger):
    return MusicBackend(http_url, cache, logger) if http_url else None


def build_voice_backend(stt_url: str | None, tts_url: str | None, cache: SimpleDiskCache, logger: JsonlLogger):
    return VoiceBackend(stt_url, tts_url, cache, logger)


