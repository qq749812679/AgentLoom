from __future__ import annotations

import time
from typing import List, Dict, Any, Optional
import requests
from ..core.logger import JsonlLogger


class HueController:
    def __init__(self, bridge_ip: str, username: str, logger: JsonlLogger) -> None:
        self.bridge_ip = bridge_ip
        self.username = username
        self.logger = logger
        self.base_url = f"http://{bridge_ip}/api/{username}"
        
    def get_lights(self) -> Dict[str, Any]:
        try:
            resp = requests.get(f"{self.base_url}/lights", timeout=5)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            self.logger.log({"event": "hue.get_lights.error", "error": str(e)})
            return {}
    
    def set_light_color(self, light_id: str, r: int, g: int, b: int, brightness: int = 254, transition_time: int = 4) -> bool:
        # Convert RGB to XY color space (simplified)
        def rgb_to_xy(r: int, g: int, b: int) -> tuple[float, float]:
            # Simplified conversion, real implementation should use proper color space conversion
            r, g, b = r/255.0, g/255.0, b/255.0
            x = r * 0.649 + g * 0.103 + b * 0.2
            y = r * 0.234 + g * 0.743 + b * 0.023
            return (x, y)
        
        x, y = rgb_to_xy(r, g, b)
        
        payload = {
            "on": True,
            "xy": [x, y],
            "bri": max(1, min(254, brightness)),
            "transitiontime": transition_time
        }
        
        try:
            resp = requests.put(f"{self.base_url}/lights/{light_id}/state", 
                              json=payload, timeout=5)
            resp.raise_for_status()
            self.logger.log({"event": "hue.set_color.ok", "light": light_id, "rgb": [r,g,b]})
            return True
        except Exception as e:
            self.logger.log({"event": "hue.set_color.error", "light": light_id, "error": str(e)})
            return False
    
    def play_lighting_sequence(self, frames: List[Dict[str, int]], light_ids: List[str]) -> bool:
        try:
            for frame in frames:
                r, g, b, ms = frame["r"], frame["g"], frame["b"], frame["ms"]
                for light_id in light_ids:
                    self.set_light_color(light_id, r, g, b, transition_time=max(1, ms//100))
                time.sleep(ms / 1000.0)
            return True
        except Exception as e:
            self.logger.log({"event": "hue.sequence.error", "error": str(e)})
            return False
