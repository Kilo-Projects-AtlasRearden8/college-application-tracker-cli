"""Date math helpers for deadlines and alerts."""

from __future__ import annotations

from datetime import date, datetime, timedelta

ISO_FORMAT = "%Y-%m-%d"


def parse_date(value: str) -> date | None:
    """Parse an ISO date string. Returns None if empty or invalid."""
    if not value:
        return None
    try:
        return datetime.strptime(value, ISO_FORMAT).date()
    except (ValueError, TypeError):
        return None


def is_valid_date(value: str) -> bool:
    return parse_date(value) is not None


def days_until(deadline_str: str, reference: date | None = None) -> int | None:
    """Days from reference (default today) to the deadline. Negative = overdue."""
    d = parse_date(deadline_str)
    if d is None:
        return None
    ref = reference or date.today()
    return (d - ref).days


def is_overdue(deadline_str: str, reference: date | None = None) -> bool:
    days = days_until(deadline_str, reference)
    return days is not None and days < 0


def is_due_today(deadline_str: str, reference: date | None = None) -> bool:
    days = days_until(deadline_str, reference)
    return days == 0


def is_due_soon(deadline_str: str, within: int = 7, reference: date | None = None) -> bool:
    """True if the deadline is today or within `within` days (not overdue-only)."""
    days = days_until(deadline_str, reference)
    return days is not None and 0 <= days <= within


def upcoming(deadlines: list[str], within: int = 7, reference: date | None = None) -> list[tuple[str, int]]:
    """Return (deadline_str, days_until) for items due today or within `within` days, sorted."""
    ref = reference or date.today()
    result: list[tuple[str, int]] = []
    for d in deadlines:
        days = days_until(d, ref)
        if days is not None and 0 <= days <= within:
            result.append((d, days))
    result.sort(key=lambda item: item[1])
    return result
