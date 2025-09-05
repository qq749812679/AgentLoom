from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Any

from ..core.logger import JsonlLogger


@dataclass
class BackendProfile:
    name: str
    kind: str  # image/music/speech
    endpoint: str
    cost_per_call_usd: float | None = None
    avg_latency_ms: float | None = None
    success_rate: float | None = None
    enabled: bool = True


class BackendRegistry:
    def __init__(self, logger: JsonlLogger) -> None:
        self.logger = logger
        self._profiles: Dict[str, BackendProfile] = {}

    def register(self, key: str, profile: BackendProfile) -> None:
        self._profiles[key] = profile
        self.logger.log({"event": "backend.register", "key": key, "profile": profile.__dict__})

    def set_enabled(self, key: str, enabled: bool) -> None:
        if key in self._profiles:
            self._profiles[key].enabled = enabled

    def list(self) -> Dict[str, BackendProfile]:
        return self._profiles

    def probe_latency(self, key: str, fn: Callable[[], Any]) -> float | None:
        if key not in self._profiles:
            return None
        t0 = time.time()
        ok = False
        try:
            fn()
            ok = True
        except Exception as e:
            self.logger.log({"event": "backend.probe.error", "key": key, "error": str(e)})
        ms = (time.time() - t0) * 1000
        p = self._profiles[key]
        p.avg_latency_ms = ms
        p.success_rate = (p.success_rate or 1.0) * 0.9 + (1.0 if ok else 0.0) * 0.1
        self.logger.log({"event": "backend.probe", "key": key, "latency_ms": ms, "ok": ok})
        return ms 