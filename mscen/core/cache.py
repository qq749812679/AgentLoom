from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Optional


def _hash_key(payload: dict[str, Any]) -> str:
    dumped = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(dumped.encode("utf-8")).hexdigest()[:16]


class SimpleDiskCache:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def get_path(self, namespace: str, payload: dict[str, Any]) -> Path:
        key = _hash_key(payload)
        ns_dir = self.root / namespace
        ns_dir.mkdir(parents=True, exist_ok=True)
        return ns_dir / f"{key}.bin"

    def exists(self, namespace: str, payload: dict[str, Any]) -> Optional[Path]:
        path = self.get_path(namespace, payload)
        return path if path.exists() else None

    def write_bytes(self, namespace: str, payload: dict[str, Any], data: bytes) -> Path:
        path = self.get_path(namespace, payload)
        path.write_bytes(data)
        return path



