"""Data models for college applications."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id() -> str:
    return uuid.uuid4().hex[:8]


@dataclass
class Essay:
    title: str
    prompt: str = ""
    status: str = "not started"  # not started | draft | done
    word_count: int = 0

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Essay":
        return Essay(
            title=data.get("title", ""),
            prompt=data.get("prompt", ""),
            status=data.get("status", "not started"),
            word_count=int(data.get("word_count", 0) or 0),
        )


@dataclass
class Recommendation:
    name: str
    role: str = ""
    status: str = "not requested"  # not requested | requested | received

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Recommendation":
        return Recommendation(
            name=data.get("name", ""),
            role=data.get("role", ""),
            status=data.get("status", "not requested"),
        )


@dataclass
class Application:
    id: str
    college: str
    deadline: str  # ISO date string (YYYY-MM-DD)
    status: str = "not started"  # not started | in progress | submitted | withdrawn
    requirements: list[str] = field(default_factory=list)
    essays: list[Essay] = field(default_factory=list)
    recommendations: list[Recommendation] = field(default_factory=list)
    notes: str = ""
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "college": self.college,
            "deadline": self.deadline,
            "status": self.status,
            "requirements": list(self.requirements),
            "essays": [e.to_dict() for e in self.essays],
            "recommendations": [r.to_dict() for r in self.recommendations],
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "Application":
        return Application(
            id=data.get("id", _new_id()),
            college=data.get("college", ""),
            deadline=data.get("deadline", ""),
            status=data.get("status", "not started"),
            requirements=list(data.get("requirements", []) or []),
            essays=[Essay.from_dict(e) for e in (data.get("essays") or [])],
            recommendations=[
                Recommendation.from_dict(r) for r in (data.get("recommendations") or [])
            ],
            notes=data.get("notes", ""),
            created_at=data.get("created_at") or _now_iso(),
            updated_at=data.get("updated_at") or _now_iso(),
        )
