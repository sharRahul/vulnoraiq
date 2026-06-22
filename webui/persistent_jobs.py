from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock
from typing import Any


@dataclass(slots=True)
class PersistedScanEvent:
    timestamp: str
    stage: str
    message: str
    progress: int
    level: str = "info"


@dataclass(slots=True)
class PersistedScanJob:
    id: str
    target: str
    profile: str
    authorised: bool
    created_by: str = "anonymous"
    status: str = "queued"
    progress: int = 0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    started_at: str | None = None
    completed_at: str | None = None
    error: str | None = None
    events: list[PersistedScanEvent] = field(default_factory=list)
    outputs: dict[str, str] = field(default_factory=dict)
    summary: dict[str, Any] = field(default_factory=dict)

    def add_event(self, stage: str, message: str, progress: int, level: str = "info") -> None:
        self.progress = progress
        self.events.append(PersistedScanEvent(datetime.now(timezone.utc).isoformat(), stage, message, progress, level))

    def to_dict(self, include_events: bool = True) -> dict[str, Any]:
        data = asdict(self)
        if not include_events:
            data.pop("events", None)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PersistedScanJob":
        events = [PersistedScanEvent(**event) for event in data.get("events", [])]
        data = {**data, "events": events}
        return cls(**data)


class PersistentJobStore:
    """JSON-backed scan job store for Web UI history persistence."""

    def __init__(self, path: str | Path = "reports/output/webui/jobs.json") -> None:
        self.path = Path(path)
        self._lock = RLock()
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def create(self, target: str, profile: str, authorised: bool, created_by: str = "anonymous") -> PersistedScanJob:
        job = PersistedScanJob(uuid.uuid4().hex[:12], target, profile, authorised, created_by=created_by)
        job.add_event("queued", "Scan queued and waiting for worker thread.", 0)
        with self._lock:
            jobs = self._load_all()
            jobs[job.id] = job
            self._save_all(jobs)
        return job

    def get(self, job_id: str) -> PersistedScanJob | None:
        with self._lock:
            return self._load_all().get(job_id)

    def list(self) -> list[PersistedScanJob]:
        with self._lock:
            return sorted(self._load_all().values(), key=lambda item: item.created_at, reverse=True)

    def update(self, job_id: str, fn) -> PersistedScanJob | None:
        with self._lock:
            jobs = self._load_all()
            job = jobs.get(job_id)
            if not job:
                return None
            fn(job)
            jobs[job_id] = job
            self._save_all(jobs)
            return job

    def _load_all(self) -> dict[str, PersistedScanJob]:
        if not self.path.exists():
            return {}
        raw = json.loads(self.path.read_text(encoding="utf-8") or "{}")
        return {job_id: PersistedScanJob.from_dict(value) for job_id, value in raw.items()}

    def _save_all(self, jobs: dict[str, PersistedScanJob]) -> None:
        self.path.write_text(
            json.dumps({job_id: job.to_dict() for job_id, job in jobs.items()}, indent=2, sort_keys=True),
            encoding="utf-8",
        )
