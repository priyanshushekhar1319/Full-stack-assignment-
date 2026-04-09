from __future__ import annotations

import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from task_manager.task_store import TaskNotFoundError, TaskStore
from task_manager.validation import validate_task_title, validate_task_update


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = BASE_DIR / "data"
STORE = TaskStore(DATA_DIR / "tasks.json")


class TaskManagerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/tasks":
            self._send_json(
                HTTPStatus.OK,
                {"success": True, "data": STORE.list_tasks()},
            )
            return

        if path == "/":
            self.path = "/index.html"

        super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/tasks":
            self._send_json(HTTPStatus.NOT_FOUND, {"success": False, "error": "Route not found."})
            return

        payload = self._read_json_body()
        if isinstance(payload, str):
            self._send_json(HTTPStatus.BAD_REQUEST, {"success": False, "error": payload})
            return

        error = validate_task_title(payload)
        if error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"success": False, "error": error})
            return

        task = STORE.create_task(payload["title"])
        self._send_json(HTTPStatus.CREATED, {"success": True, "data": task})

    def do_PATCH(self):
        task_id = self._extract_task_id()
        if task_id is None:
            self._send_json(HTTPStatus.NOT_FOUND, {"success": False, "error": "Route not found."})
            return

        payload = self._read_json_body()
        if isinstance(payload, str):
            self._send_json(HTTPStatus.BAD_REQUEST, {"success": False, "error": payload})
            return

        error = validate_task_update(payload)
        if error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"success": False, "error": error})
            return

        try:
            task = STORE.update_task_status(task_id, payload["completed"])
        except TaskNotFoundError as exc:
            self._send_json(HTTPStatus.NOT_FOUND, {"success": False, "error": str(exc)})
            return

        self._send_json(HTTPStatus.OK, {"success": True, "data": task})

    def do_DELETE(self):
        task_id = self._extract_task_id()
        if task_id is None:
            self._send_json(HTTPStatus.NOT_FOUND, {"success": False, "error": "Route not found."})
            return

        try:
            task = STORE.delete_task(task_id)
        except TaskNotFoundError as exc:
            self._send_json(HTTPStatus.NOT_FOUND, {"success": False, "error": str(exc)})
            return

        self._send_json(HTTPStatus.OK, {"success": True, "data": task})

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.end_headers()

    def _extract_task_id(self):
        path = urlparse(self.path).path.strip("/")
        parts = path.split("/")
        if len(parts) == 2 and parts[0] == "tasks" and parts[1]:
            return parts[1]
        return None

    def _read_json_body(self):
        content_length = self.headers.get("Content-Length")
        if content_length is None:
            return "Request body is required."

        try:
            body = self.rfile.read(int(content_length))
            return json.loads(body.decode("utf-8"))
        except ValueError:
            return "Request body must be valid JSON."

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run(server_class=ThreadingHTTPServer, handler_class=TaskManagerHandler):
    server = server_class(("127.0.0.1", 8000), handler_class)
    print("Task Manager running at http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    run()
