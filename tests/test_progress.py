"""Tests for progress tracking."""

from college_tracker.models import Application, Essay, Recommendation
from college_tracker.progress import (
    application_percent,
    application_progress,
    overall_percent,
    overall_progress,
    status_counts,
)


def _app(essays=None, recommendations=None, requirements=None, status="not started"):
    return Application(
        id="app1",
        college="Test College",
        deadline="2026-11-01",
        status=status,
        essays=essays or [],
        recommendations=recommendations or [],
        requirements=requirements or [],
    )


def test_no_tracked_items_derives_from_status():
    app = _app()
    assert application_progress(app) == 0.0
    assert application_percent(app) == 0

    app.status = "in progress"
    assert application_progress(app) == 0.5
    assert application_percent(app) == 50

    app.status = "submitted"
    assert application_progress(app) == 1.0
    assert application_percent(app) == 100


def test_essays_done_weight_50_percent():
    app = _app(
        essays=[Essay(title="Personal Statement", status="done")],
        recommendations=[],
        requirements=[],
    )
    assert application_progress(app) == 0.5
    assert application_percent(app) == 50

    app.essays[0].status = "draft"
    assert application_progress(app) == 0.0


def test_recommendations_received_weight_30_percent():
    app = _app(
        essays=[],
        recommendations=[Recommendation(name="Ms. Teacher", status="received")],
        requirements=[],
    )
    assert application_progress(app) == 0.3
    assert application_percent(app) == 30

    app.recommendations[0].status = "requested"
    assert application_progress(app) == 0.0


def test_requirements_submitted_weight_20_percent():
    app = _app(
        essays=[],
        recommendations=[],
        requirements=["transcript"],
        status="submitted",
    )
    assert application_progress(app) == 0.2
    assert application_percent(app) == 20


def test_combined_progress():
    app = _app(
        essays=[Essay(title="S1", status="done")],
        recommendations=[Recommendation(name="T1", status="received")],
        requirements=["transcript"],
        status="submitted",
    )
    assert application_progress(app) == 1.0
    assert application_percent(app) == 100


def test_overall_empty():
    assert overall_progress([]) == 0.0
    assert overall_percent([]) == 0


def test_overall_multiple():
    a1 = _app(essays=[Essay(title="S1", status="done")], status="submitted")
    a2 = _app(essays=[Essay(title="S2", status="not started")], status="not started")
    pct = overall_percent([a1, a2])
    assert pct == 25


def test_status_counts():
    a1 = _app(status="submitted")
    a2 = _app(status="in progress")
    a3 = _app(status="submitted")
    counts = status_counts([a1, a2, a3])
    assert counts == {"submitted": 2, "in progress": 1}
