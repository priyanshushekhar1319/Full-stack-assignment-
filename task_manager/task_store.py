"""Small file-backed task storage layer."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


class TaskNotFoundError(Exception):
    """Raised when a task id is not present in storage."""


class TaskStore:
    def __init__(self, storage_path):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._tasks = self._load()

    def list_tasks(self):
        return sorted(self._tasks, key=lambda task: task["createdAt"], reverse=True)

    def create_task(self, title):
        task = {
            "id": str(uuid.uuid4()),
            "title": title.strip(),
            "completed": False,
            "createdAt": datetime.now(timezone.utc).isoformat(),
        }
        self._tasks.append(task)
        self._save()
        return task

    def update_task_status(self, task_id, completed):
        task = self._find_task(task_id)
        task["completed"] = completed
        self._save()
        return task

    def delete_task(self, task_id):
        task = self._find_task(task_id)
        self._tasks = [item for item in self._tasks if item["id"] != task_id]
        self._save()
        return task

    def _find_task(self, task_id):
        for task in self._tasks:
            if task["id"] == task_id:
                return task
        raise TaskNotFoundError(f"Task '{task_id}' was not found.")

    def _load(self):
        if not self.storage_path.exists():
            return []

        try:
            with self.storage_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            return []

        if not isinstance(data, list):
            return []

        tasks = []
        for item in data:
            if not isinstance(item, dict):
                continue

            if not all(key in item for key in ("id", "title", "completed", "createdAt")):
                continue

            tasks.append(
                {
                    "id": str(item["id"]),
                    "title": str(item["title"]).strip(),
                    "completed": bool(item["completed"]),
                    "createdAt": str(item["createdAt"]),
                }
            )

        return tasks

    def _save(self):
        with self.storage_path.open("w", encoding="utf-8") as file:
            json.dump(self._tasks, file, indent=2)
