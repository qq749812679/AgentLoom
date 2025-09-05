from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, List


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    FAILED = "failed"
    COMPLETED = "completed"


@dataclass
class Task:
    id: str
    kind: str
    params: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    progress: float = 0.0
    error: Optional[str] = None


class TaskQueue:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.state_file = base_dir / "tasks" / "queue.jsonl"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.tasks: Dict[str, Task] = {}
        self._load()

    def _load(self) -> None:
        if not self.state_file.exists():
            return
        for line in self.state_file.read_text(encoding="utf-8").splitlines():
            try:
                data = json.loads(line)
                self.tasks[data["id"]] = Task(**data)
            except Exception:
                continue

    def _persist(self) -> None:
        with self.state_file.open("w", encoding="utf-8") as f:
            for t in self.tasks.values():
                f.write(json.dumps(asdict(t), ensure_ascii=False) + "\n")

    def submit(self, kind: str, params: Dict[str, Any]) -> Task:
        tid = str(uuid.uuid4())[:8]
        task = Task(id=tid, kind=kind, params=params)
        self.tasks[tid] = task
        self._persist()
        return task

    def pause(self, task_id: str) -> None:
        t = self.tasks.get(task_id)
        if t and t.status == TaskStatus.RUNNING:
            t.status = TaskStatus.PAUSED
            self._persist()

    def resume(self, task_id: str) -> None:
        t = self.tasks.get(task_id)
        if t and t.status in (TaskStatus.PAUSED, TaskStatus.FAILED):
            t.status = TaskStatus.PENDING
            t.error = None
            self._persist()

    def retry(self, task_id: str) -> None:
        self.resume(task_id)

    def update(self, task_id: str, *, status: Optional[TaskStatus] = None, progress: Optional[float] = None, error: Optional[str] = None) -> None:
        t = self.tasks.get(task_id)
        if not t:
            return
        if status is not None:
            t.status = status
        if progress is not None:
            t.progress = progress
        if error is not None:
            t.error = error
        self._persist()

    def list(self) -> List[Task]:
        return list(self.tasks.values())

    def get(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id) 