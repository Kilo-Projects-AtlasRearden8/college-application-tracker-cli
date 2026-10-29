"""Progress tracking for applications."""

from __future__ import annotations

from .models import Application, Essay, Recommendation

ESSAY_WEIGHT = 0.5
RECOMMENDATION_WEIGHT = 0.3
REQUIREMENT_WEIGHT = 0.2


def item_progress(value: str, done_values: tuple[str, ...] = ("done", "received", "submitted")) -> float:
    return 1.0 if value in done_values else 0.0


def application_progress(app: Application) -> float:
    """Completion fraction for a single application (0.0 to 1.0).

    Weighted: essays 50%, recommendations 30%, requirements 20%.
    An application with no tracked items scores 0.0 until something is added.
    """
    essay_score = 0.0
    if app.essays:
        essay_score = sum(item_progress(e.status, ("done",)) for e in app.essays) / len(app.essays)

    rec_score = 0.0
    if app.recommendations:
        rec_score = sum(item_progress(r.status, ("received",)) for r in app.recommendations) / len(app.recommendations)

    req_score = 0.0
    if app.requirements:
        # Requirements are tracked as free text; mark done only when the app
        # itself is submitted, otherwise count each requirement as pending.
        req_score = 1.0 if app.status == "submitted" else 0.0

    weighted = (
        essay_score * ESSAY_WEIGHT
        + rec_score * RECOMMENDATION_WEIGHT
        + req_score * REQUIREMENT_WEIGHT
    )

    if not app.essays and not app.recommendations and not app.requirements:
        # Nothing tracked yet; derive progress from status alone.
        return {"not started": 0.0, "in progress": 0.5, "submitted": 1.0, "withdrawn": 1.0}.get(
            app.status, 0.0
        )
    return weighted


def application_percent(app: Application) -> int:
    return int(round(application_progress(app) * 100))


def overall_progress(apps: list[Application]) -> float:
    if not apps:
        return 0.0
    return sum(application_progress(a) for a in apps) / len(apps)


def overall_percent(apps: list[Application]) -> int:
    return int(round(overall_progress(apps) * 100))


def status_counts(apps: list[Application]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for app in apps:
        counts[app.status] = counts.get(app.status, 0) + 1
    return counts
