from pathlib import Path
import unittest

from task_manager.task_store import TaskNotFoundError, TaskStore
from task_manager.validation import validate_task_title, validate_task_update


class TaskStoreTests(unittest.TestCase):
    def setUp(self):
        self.test_root = Path(__file__).resolve().parents[1] / ".tmp_tests"
        self.test_root.mkdir(exist_ok=True)
        self.storage_path = self.test_root / "tasks.json"
        if self.storage_path.exists():
            self.storage_path.unlink()
        self.store = TaskStore(self.storage_path)

    def tearDown(self):
        if self.storage_path.exists():
            self.storage_path.unlink()

    def test_create_task_persists_data(self):
        task = self.store.create_task("Write README")

        self.assertEqual(task["title"], "Write README")
        self.assertFalse(task["completed"])
        reloaded = TaskStore(self.storage_path)
        self.assertEqual(len(reloaded.list_tasks()), 1)

    def test_update_task_status_changes_completed_flag(self):
        task = self.store.create_task("Ship feature")

        updated = self.store.update_task_status(task["id"], True)

        self.assertTrue(updated["completed"])

    def test_delete_missing_task_raises_error(self):
        with self.assertRaises(TaskNotFoundError):
            self.store.delete_task("missing-id")


class ValidationTests(unittest.TestCase):
    def test_validate_task_title_requires_non_empty_string(self):
        self.assertIsNotNone(validate_task_title({"title": ""}))
        self.assertIsNotNone(validate_task_title({"title": 123}))
        self.assertIsNone(validate_task_title({"title": "Valid task"}))

    def test_validate_task_update_accepts_boolean_completed_only(self):
        self.assertIsNone(validate_task_update({"completed": True}))
        self.assertIsNotNone(validate_task_update({"completed": "yes"}))
        self.assertIsNotNone(validate_task_update({"title": "Nope"}))


if __name__ == "__main__":
    unittest.main()
