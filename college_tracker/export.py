"""CSV export for college applications."""

from __future__ import annotations

import csv
from typing import Iterable

from .models import Application, Essay, Recommendation


def _join(items: Iterable[str]) -> str:
    return "; ".join(str(i) for i in items if i)


def export_csv(apps: Iterable[Application], path: str) -> None:
    """Write applications to a CSV file.

    Columns: id, college, deadline, status, requirements, essays,
    recommendations, notes, created_at, updated_at
    """
    fieldnames = [
        "id",
        "college",
        "deadline",
        "status",
        "requirements",
        "essays",
        "recommendations",
        "notes",
        "created_at",
        "updated_at",
    ]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for app in apps:
            writer.writerow(
                {
                    "id": app.id,
                    "college": app.college,
                    "deadline": app.deadline,
                    "status": app.status,
                    "requirements": _join(app.requirements),
                    "essays": _join(f"{e.title} ({e.status})" for e in app.essays),
                    "recommendations": _join(
                        f"{r.name} ({r.status})" for r in app.recommendations
                    ),
                    "notes": app.notes,
                    "created_at": app.created_at,
                    "updated_at": app.updated_at,
                }
            )
