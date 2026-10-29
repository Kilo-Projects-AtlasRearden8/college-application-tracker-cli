"""Tests for the CLI."""

import os
import sys

from college_tracker.cli import main


def test_help_runs(capsys):
    try:
        main(["--help"])
    except SystemExit as exc:
        assert exc.code == 0
    captured = capsys.readouterr()
    assert "Track college applications" in captured.out


def test_add_and_list(tmp_path, monkeypatch, capsys):
    data_path = str(tmp_path / "apps.json")
    monkeypatch.setattr("college_tracker.cli.DEFAULT_DATA_PATH", data_path)
    code = main(["--data", data_path, "add", "State U", "2026-11-01", "--status", "in progress"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Added State U" in captured.out

    code = main(["--data", data_path, "list"])
    assert code == 0
    captured = capsys.readouterr()
    assert "State U" in captured.out


def test_alerts_no_data(tmp_path, capsys):
    data_path = str(tmp_path / "apps.json")
    code = main(["--data", data_path, "alerts", "--within", "7"])
    assert code == 0
    captured = capsys.readouterr()
    assert "No due-date alerts" in captured.out


def test_progress_no_data(tmp_path, capsys):
    data_path = str(tmp_path / "apps.json")
    code = main(["--data", data_path, "progress"])
    assert code == 0
    captured = capsys.readouterr()
    assert "No applications tracked yet" in captured.out


def test_export(tmp_path, capsys):
    data_path = str(tmp_path / "apps.json")
    out_path = str(tmp_path / "apps.csv")
    main(["--data", data_path, "add", "State U", "2026-11-01", "--status", "submitted"])
    code = main(["--data", data_path, "export", out_path])
    assert code == 0
    captured = capsys.readouterr()
    assert "Exported" in captured.out
    assert os.path.exists(out_path)
