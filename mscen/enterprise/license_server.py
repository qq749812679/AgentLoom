from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class LicenseInfo:
    edition: str  # community / enterprise
    key: Optional[str] = None


class LicenseServer:
    def __init__(self, base_dir: Path) -> None:
        self.lic_file = base_dir / "license.json"
        self.info = self._load()

    def _load(self) -> LicenseInfo:
        if self.lic_file.exists():
            data = json.loads(self.lic_file.read_text(encoding="utf-8"))
            return LicenseInfo(**data)
        return LicenseInfo(edition="community")

    def save(self, info: LicenseInfo) -> None:
        self.lic_file.write_text(json.dumps(info.__dict__, ensure_ascii=False, indent=2), encoding="utf-8")
        self.info = info

    def is_enterprise(self) -> bool:
        return self.info.edition == "enterprise" 