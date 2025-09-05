from __future__ import annotations

import time
from typing import List, Dict, Any
import requests
from ..core.logger import JsonlLogger


class WLEDController:
    def __init__(self, device_ip: str, logger: JsonlLogger) -> None:
        self.device_ip = device_ip
        self.logger = logger
        self.base_url = f"http://{device_ip}"
        
    def get_info(self) -> Dict[str, Any]:
        try:
            resp = requests.get(f"{self.base_url}/json/info", timeout=5)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            self.logger.log({"event": "wled.get_info.error", "error": str(e)})
            return {}
    
    def set_color(self, r: int, g: int, b: int, brightness: int = 255) -> bool:
        payload = {
            "on": True,
            "bri": max(1, min(255, brightness)),
            "seg": [{"col": [[r, g, b]]}]
        }
        
        try:
            resp = requests.post(f"{self.base_url}/json/state", 
                               json=payload, timeout=5)
            resp.raise_for_status()
            self.logger.log({"event": "wled.set_color.ok", "rgb": [r,g,b]})
            return True
        except Exception as e:
            self.logger.log({"event": "wled.set_color.error", "error": str(e)})
            return False
    
    def play_lighting_sequence(self, frames: List[Dict[str, int]]) -> bool:
        try:
            for frame in frames:
                r, g, b, ms = frame["r"], frame["g"], frame["b"], frame["ms"]
                self.set_color(r, g, b)
                time.sleep(ms / 1000.0)
            return True
        except Exception as e:
            self.logger.log({"event": "wled.sequence.error", "error": str(e)})
            return False
    
    def emergency_stop(self) -> bool:
        payload = {"on": False}
        try:
            resp = requests.post(f"{self.base_url}/json/state", 
                               json=payload, timeout=5)
            resp.raise_for_status()
            self.logger.log({"event": "wled.emergency_stop.ok"})
            return True
        except Exception as e:
            self.logger.log({"event": "wled.emergency_stop.error", "error": str(e)})
            return False
