from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any
from ..core.logger import JsonlLogger


@dataclass
class AccessContext:
    user_id: str
    role: str  # viewer/editor/admin


class SecurityManager:
    def __init__(self, base_dir: Path) -> None:
        self.log = JsonlLogger(base_dir / "logs", name="audit")

    def check_permission(self, ctx: AccessContext, action: str, resource: str) -> bool:
        allowed = ctx.role in ("admin", "editor") or (ctx.role == "viewer" and action in ("read",))
        self.log.log({"event": "authz.check", "user": ctx.user_id, "role": ctx.role, "action": action, "resource": resource, "allowed": allowed})
        return allowed

    def record_event(self, ctx: Optional[AccessContext], event: str, details: Dict[str, Any]) -> None:
        self.log.log({"event": event, "user": getattr(ctx, "user_id", None), **details}) 