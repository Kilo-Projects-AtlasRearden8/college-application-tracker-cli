# STATUS

College Application Tracker CLI — Asdale Dynamics, LLC

## What was built

A local-first Python command-line tool to track college applications: deadlines, requirements, essays, and recommendation letters.

Package: `college_tracker`
- `models.py` — `Application`, `Essay`, `Recommendation` dataclasses with JSON serialization.
- `storage.py` — `Storage`: read/write applications to a local JSON file (atomic write via tmp + replace).
- `dates.py` — date math: parse, days until, overdue, due today, due soon, upcoming (sorted).
- `progress.py` — weighted progress tracking (essays 50%, recommendations 30%, requirements 20%) plus overall and status counts.
- `alerts.py` — due-date alerts (overdue / due today / due soon).
- `export.py` — CSV export of all applications.
- `cli.py` — argparse CLI: add, list, show, update, delete, export, alerts, progress, des. Global `--data` option selects the JSON file.

Tests: `tests/` — 26 tests covering date math, progress tracking, storage round-trip, and CLI behavior.

Packaging: `pyproject.toml` (setuptools, `college-tracker` console script).
Docs: `README.md`, `LICENSE` (MIT, Copyright (c) 2026 Asdale Dynamics, LLC), `STATUS.md`.

## How to run

Install:
```bash
pip install .
```

Run directly from source:
```bash
python -m college_tracker.cli --help
```

Add an application:
```bash
college-tracker add "State University" 2026-11-01 --status "in progress" \
  --requirements "transcript,test scores,essay" --notes "early action"
```

List applications:
```bash
college-tracker list
```

Check due-date alerts:
```bash
college-tracker alerts --within 7
```

View progress:
```bash
college-tracker progress
```

Export to CSV:
```bash
college-tracker export applications.csv
```

Data is stored locally in `data/applications.json` by default; use `--data <path>` to choose another file.

## Verification results

- `pytest`: 26 passed (date math, progress tracking, storage, CLI).
- `python -m college_tracker.cli --help`: runs, prints usage.
- End-to-end CLI exercised: add, list, show, alerts, progress, export — all produce correct output.
- `pip install .`: builds and installs the wheel successfully.
- No API keys, secrets, or personal data in any file.
- No `.github/workflows` files added.

## Known gaps

- No essay/recommendation add/edit subcommands yet (must edit via JSON directly or `update` on top-level fields only).
- Progress for requirements counts as done only when the application status is "submitted" (free-text requirements have no per-item status).
- No test for `alerts`, `export`, or `storage` CLI output beyond basic smoke checks.
- Packaging install requires `--break-system-packages` on externally-managed Python environments; use a venv otherwise.
