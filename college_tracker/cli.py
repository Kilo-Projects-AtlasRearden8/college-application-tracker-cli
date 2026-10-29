"""Command-line interface for the college application tracker."""

from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from .alerts import check_alerts
from .dates import days_until, is_overdue
from .export import export_csv
from .models import Application, Essay, Recommendation
from .progress import application_percent, overall_percent, status_counts
from .storage import Storage


DEFAULT_DATA_PATH = "data/applications.json"


def _new_app_id() -> str:
    import uuid

    return uuid.uuid4().hex[:8]


def cmd_add(args: argparse.Namespace, storage: Storage) -> int:
    app = Application(
        id=_new_app_id(),
        college=args.college,
        deadline=args.deadline,
        status=args.status,
        requirements=[r.strip() for r in args.requirements.split(",") if r.strip()]
        if args.requirements
        else [],
        notes=args.notes or "",
    )
    storage.save(app)
    print(f"Added {args.college} (id={app.id}).")
    return 0


def cmd_list(args: argparse.Namespace, storage: Storage) -> int:
    apps = storage.list_all()
    if not apps:
        print("No applications tracked yet.")
        return 0
    for app in apps:
        days = days_until(app.deadline)
        overdue = " (OVERDUE)" if is_overdue(app.deadline) else ""
        due = f" due in {days} day(s)" if days is not None else ""
        print(
            f"{app.id} | {app.college} | {app.deadline}{due}{overdue} | {app.status} | {application_percent(app)}%"
        )
    return 0


def cmd_show(args: argparse.Namespace, storage: Storage) -> int:
    app = storage.get(args.id)
    if not app:
        print(f"No application with id {args.id}.")
        return 1
    print(f"ID:        {app.id}")
    print(f"College:   {app.college}")
    print(f"Deadline:  {app.deadline}")
    print(f"Status:    {app.status}")
    print(f"Progress:  {application_percent(app)}%")
    if app.requirements:
        print("Requirements:")
        for req in app.requirements:
            print(f"  - {req}")
    if app.essays:
        print("Essays:")
        for e in app.essays:
            print(f"  - {e.title} [{e.status}] ({e.word_count} words)")
    if app.recommendations:
        print("Recommendations:")
        for r in app.recommendations:
            print(f"  - {r.name} ({r.role}) [{r.status}]")
    if app.notes:
        print(f"Notes:     {app.notes}")
    print(f"Created:   {app.created_at}")
    print(f"Updated:   {app.updated_at}")
    return 0


def cmd_update(args: argparse.Namespace, storage: Storage) -> int:
    app = storage.get(args.id)
    if not app:
        print(f"No application with id {args.id}.")
        return 1
    if args.college is not None:
        app.college = args.college
    if args.deadline is not None:
        app.deadline = args.deadline
    if args.status is not None:
        app.status = args.status
    if args.notes is not None:
        app.notes = args.notes
    storage.save(app)
    print(f"Updated {app.id}.")
    return 0


def cmd_delete(args: argparse.Namespace, storage: Storage) -> int:
    if storage.delete(args.id):
        print(f"Deleted {args.id}.")
        return 0
    print(f"No application with id {args.id}.")
    return 1


def cmd_export(args: argparse.Namespace, storage: Storage) -> int:
    apps = storage.list_all()
    export_csv(apps, args.path)
    print(f"Exported {len(apps)} application(s) to {args.path}.")
    return 0


def cmd_alerts(args: argparse.Namespace, storage: Storage) -> int:
    apps = storage.list_all()
    alerts = check_alerts(apps, within=args.within)
    if not alerts:
        print("No due-date alerts.")
        return 0
    for alert in alerts:
        print(alert.message())
    return 0


def cmd_progress(args: argparse.Namespace, storage: Storage) -> int:
    apps = storage.list_all()
    if not apps:
        print("No applications tracked yet.")
        return 0
    print(f"Overall progress: {overall_percent(apps)}%")
    counts = status_counts(apps)
    for status in sorted(counts):
        print(f"  {status}: {counts[status]}")
    print("\nPer-application:")
    for app in apps:
        print(f"  {app.id} | {app.college} | {application_percent(app)}%")
    return 0


def cmd_due(args: argparse.Namespace, storage: Storage) -> int:
    apps = storage.list_all()
    from .dates import upcoming

    items = upcoming([a.deadline for a in apps], within=args.within)
    if not items:
        print("No upcoming deadlines.")
        return 0
    by_id = {a.deadline: a for a in apps}
    for deadline, days in items:
        app = by_id.get(deadline)
        college = app.college if app else "(unknown)"
        print(f"{deadline} | {college} | due in {days} day(s)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="college-tracker",
        description="Track college applications: deadlines, requirements, essays, recommendations.",
    )
    parser.add_argument(
        "--data",
        default=DEFAULT_DATA_PATH,
        help=f"Path to JSON storage file (default: {DEFAULT_DATA_PATH})",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new application.")
    p_add.add_argument("college", help="College name.")
    p_add.add_argument("deadline", help="Deadline date (YYYY-MM-DD).")
    p_add.add_argument("--status", default="not started", help="Application status.")
    p_add.add_argument("--requirements", default="", help="Comma-separated requirements.")
    p_add.add_argument("--notes", default="", help="Notes.")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List all applications.")
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show", help="Show details for one application.")
    p_show.add_argument("id", help="Application id.")
    p_show.set_defaults(func=cmd_show)

    p_update = sub.add_parser("update", help="Update an application.")
    p_update.add_argument("id", help="Application id.")
    p_update.add_argument("--college", default=None)
    p_update.add_argument("--deadline", default=None)
    p_update.add_argument("--status", default=None)
    p_update.add_argument("--notes", default=None)
    p_update.set_defaults(func=cmd_update)

    p_delete = sub.add_parser("delete", help="Delete an application.")
    p_delete.add_argument("id", help="Application id.")
    p_delete.set_defaults(func=cmd_delete)

    p_export = sub.add_parser("export", help="Export applications to CSV.")
    p_export.add_argument("path", help="Output CSV path.")
    p_export.set_defaults(func=cmd_export)

    p_alerts = sub.add_parser("alerts", help="Show due-date alerts.")
    p_alerts.add_argument("--within", type=int, default=7, help="Days within which to alert (default 7).")
    p_alerts.set_defaults(func=cmd_alerts)

    p_progress = sub.add_parser("progress", help="Show overall progress.")
    p_progress.set_defaults(func=cmd_progress)

    p_due = sub.add_parser("due", help="Show upcoming deadlines.")
    p_due.add_argument("--within", type=int, default=30, help="Days within which to show (default 30).")
    p_due.set_defaults(func=cmd_due)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    storage = Storage(args.data)
    return args.func(args, storage)


if __name__ == "__main__":
    sys.exit(main())
