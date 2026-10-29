"""Local JSON storage for college applications."""

from __future__ import annotations

import json
import os
from typing import Optional

from .models import Application


class Storage:
    """Read/write applications to a single JSON file."""

    def __init__(self, path: str) -> None:
        self.path = path
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

    def _read_raw(self) -> list[dict]:
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (json.JSONDecodeError, OSError):
            return []
        if not isinstance(data, list):
            return []
        return [item for item in data if isinstance(item, dict)]

    def write(self, apps: list[Application]) -> None:
        payload = [app.to_dict() for app in apps]
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp, self.path)

    def load(self) -> list[Application]:
        return [Application.from_dict(item) for item in self._read_raw()]

    def save(self, app: Application) -> None:
        apps = self.load()
        for idx, existing in enumerate(apps):
            if existing.id == app.id:
                apps[idx] = app
                self.write(apps)
                return
        apps.append(app)
        self.write(apps)

    def get(self, app_id: str) -> Optional[Application]:
        for app in self.load():
            if app.id == app_id:
                return app
        return None

    def delete(self, app_id: str) -> bool:
        apps = self.load()
        filtered = [app for app in apps if app.id != app_id]
        if len(filtered) == len(apps):
            return False
        self.write(filtered)
        return True

    def list_all(self) -> list[Application]:
        return self.load()
