"""Due-date alert helpers."""

from __future__ import annotations

from dataclasses import dataclass

from .dates import days_until, is_overdue, is_due_today, is_due_soon
from .models import Application


@dataclass
class Alert:
    application_id: str
    college: str
    deadline: str
    days_until: int | None
    kind: str  # overdue | due_today | due_soon | upcoming

    def message(self) -> str:
        if self.kind == "overdue":
            return f"OVERDUE: {self.college} (deadline {self.deadline}) was {abs(self.days_until or 0)} day(s) ago."
        if self.kind == "due_today":
            return f"DUE TODAY: {self.college} (deadline {self.deadline}) is due today."
        if self.kind == "due_soon":
            return f"DUE SOON: {self.college} (deadline {self.deadline}) is due in {self.days_until} day(s)."
        return f"UPCOMING: {self.college} (deadline {self.deadline}) is due in {self.days_until} day(s)."


def check_alerts(apps: list[Application], within: int = 7, reference=None) -> list[Alert]:
    """Return alerts for applications whose deadlines are overdue or coming up."""
    alerts: list[Alert] = []
    for app in apps:
        days = days_until(app.deadline, reference)
        if days is None:
            continue
        if is_overdue(app.deadline, reference):
            alerts.append(Alert(app.id, app.college, app.deadline, days, "overdue"))
        elif is_due_today(app.deadline, reference):
            alerts.append(Alert(app.id, app.college, app.deadline, days, "due_today"))
        elif is_due_soon(app.deadline, within, reference):
            alerts.append(Alert(app.id, app.college, app.deadline, days, "due_soon"))
    alerts.sort(key=lambda a: (a.days_until is None, a.days_until or 0))
    return alerts
