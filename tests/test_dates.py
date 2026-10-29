"""Tests for date math helpers."""

from datetime import date

import pytest

from college_tracker.dates import (
    days_until,
    is_due_soon,
    is_due_today,
    is_overdue,
    is_valid_date,
    upcoming,
)


def test_parse_valid_and_invalid_dates():
    from college_tracker.dates import parse_date

    assert parse_date("2026-11-01") == date(2026, 11, 1)
    assert parse_date("") is None
    assert parse_date("not-a-date") is None
    assert parse_date("2026-13-01") is None


def test_is_valid_date():
    assert is_valid_date("2026-11-01") is True
    assert is_valid_date("") is False
    assert is_valid_date("bad") is False


def test_days_until_relative_to_today():
    today = date.today()
    assert days_until(today.isoformat()) == 0
    assert days_until((today.isoformat()), reference=today) == 0


def test_days_until_future_and_past():
    today = date.today()
    future = (today.__add__(__import__("datetime").timedelta(days=5))).isoformat()
    past = (today.__sub__(__import__("datetime").timedelta(days=3))).isoformat()
    assert days_until(future, reference=today) == 5
    assert days_until(past, reference=today) == -3


def test_is_overdue():
    today = date.today()
    assert is_overdue((today.__sub__(__import__("datetime").timedelta(days=1))).isoformat(), reference=today) is True
    assert is_overdue(today.isoformat(), reference=today) is False
    assert is_overdue((today.__add__(__import__("datetime").timedelta(days=5))).isoformat(), reference=today) is False


def test_is_due_today():
    today = date.today()
    assert is_due_today(today.isoformat(), reference=today) is True
    assert is_due_today((today.__add__(__import__("datetime").timedelta(days=1))).isoformat(), reference=today) is False


def test_is_due_soon():
    today = date.today()
    assert is_due_soon(today.isoformat(), within=7, reference=today) is True
    assert is_due_soon((today.__add__(__import__("datetime").timedelta(days=7))).isoformat(), within=7, reference=today) is True
    assert is_due_soon((today.__add__(__import__("datetime").timedelta(days=8))).isoformat(), within=7, reference=today) is False
    assert is_due_soon((today.__sub__(__import__("datetime").timedelta(days=1))).isoformat(), within=7, reference=today) is False


def test_upcoming_sorted():
    today = date.today()
    from college_tracker.dates import parse_date

    d1 = (today.__add__(__import__("datetime").timedelta(days=10))).isoformat()
    d2 = (today.__add__(__import__("datetime").timedelta(days=2))).isoformat()
    d3 = (today.__sub__(__import__("datetime").timedelta(days=1))).isoformat()
    result = upcoming([d1, d2, d3], within=10, reference=today)
    assert result == [(d2, 2), (d1, 10)]
