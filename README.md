# College Application Tracker CLI

A local-first Python command-line tool to track college applications: deadlines, requirements, essays, and recommendation letters. Built by Asdale Dynamics, LLC.

## About

This tool helps students and families keep track of college applications in one place. It stores everything locally in a JSON file, can export to CSV, and surfaces due-date alerts so nothing slips through the cracks. No accounts, no API keys, no cloud — your data stays on your machine.

Created by **Asdale Dynamics, LLC** (Indiana, formed October 2026), a beginner-friendly AI education and practical-tools company founded by Dylan Asdale, a registered nurse turned AI author. Dylan's book *The Massive AI Manual* and hub site dylanasdale.github.io explain AI "like a friend would": plain English, step by step, never condescending.

## Features

- Add, list, show, update, and delete college applications
- Track deadlines, requirements, essays, and recommendation letters per application
- Local JSON storage (your data, your machine)
- CSV export for spreadsheets or sharing
- Due-date alerts: overdue, due today, due soon
- Progress tracking per application and overall
- No accounts, no API keys, no network required

## Install

```bash
git clone <this-repo>
cd college-application-tracker-cli
pip install .
```

Or run directly without installing:

```bash
python -m college_tracker.cli --help
```

## Quick start

Add an application:

```bash
college-tracker add "State University" 2026-11-01 --status "in progress" \
  --requirements "transcript,test scores,essay" --notes "Early action"
```

List all applications:

```bash
college-tracker list
```

Show details for one application:

```bash
college-tracker show <id>
```

Check due-date alerts:

```bash
college-tracker alerts --within 7
```

Export to CSV:

```bash
college-tracker export applications.csv
```

View overall progress:

```bash
college-tracker progress
```

## Data

By default, data is stored in `data/applications.json`. Use `--data <path>` with any command to point at a different file.

## Testing

```bash
pip install pytest
pytest
```

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC.

## Credit

Built and maintained by Asdale Dynamics, LLC.
