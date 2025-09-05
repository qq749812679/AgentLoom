from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class JsonlLogger:
    def __init__(self, log_dir: Path, name: str) -> None:
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.log_dir / f"{name}.jsonl"

    def log(self, record: dict[str, Any]) -> None:
        record = {"time": datetime.utcnow().isoformat() + "Z", **record}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")



