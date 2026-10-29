"""Tests for JSON storage."""

import os
import tempfile

from college_tracker.models import Application, Essay
from college_tracker.storage import Storage


def test_save_and_load_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "apps.json")
        storage = Storage(path)
        app = Application(
            id="abc12345",
            college="State U",
            deadline="2026-11-01",
            essays=[Essay(title="Statement", status="done")],
        )
        storage.save(app)
        loaded = storage.get("abc12345")
        assert loaded is not None
        assert loaded.college == "State U"
        assert loaded.deadline == "2026-11-01"
        assert len(loaded.essays) == 1
        assert loaded.essays[0].status == "done"


def test_update_existing_app():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "apps.json")
        storage = Storage(path)
        app = Application(id="abc12345", college="State U", deadline="2026-11-01")
        storage.save(app)
        app.college = "State University"
        app.status = "submitted"
        storage.save(app)
        loaded = storage.get("abc12345")
        assert loaded.college == "State University"
        assert loaded.status == "submitted"


def test_delete_app():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "apps.json")
        storage = Storage(path)
        app = Application(id="abc12345", college="State U", deadline="2026-11-01")
        storage.save(app)
        assert storage.delete("abc12345") is True
        assert storage.get("abc12345") is None
        assert storage.delete("nonexistent") is False


def test_list_all():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "apps.json")
        storage = Storage(path)
        assert storage.list_all() == []
        storage.save(Application(id="a1", college="A", deadline="2026-11-01"))
        storage.save(Application(id="a2", college="B", deadline="2026-12-01"))
        assert len(storage.list_all()) == 2


def test_missing_file_returns_empty():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "nonexistent.json")
        storage = Storage(path)
        assert storage.list_all() == []
