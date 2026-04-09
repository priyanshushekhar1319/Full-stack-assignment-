# Task Manager

This repository contains a small full stack Task Manager built for the Full Stack Developer technical assignment. The app keeps the stack intentionally small and easy to review:

- Backend: Python standard library HTTP server
- Frontend: HTML, CSS, and vanilla JavaScript
- Storage: local JSON file persistence

No third-party packages are required.

## Assignment Coverage

Core requirements completed:

- Display a list of tasks
- Add a new task
- Mark a task as completed
- Delete a task
- Show loading and error states
- Expose a REST API
- Validate incoming data
- Return clear JSON responses
- Keep backend and frontend code organized

Optional bonus completed:

- Persist tasks after refresh
- Filter tasks by all, active, or completed
- Add basic tests

## How to Run

1. Open a terminal in the project folder.
2. Start the server:

```bash
python app.py
```

3. Open the app in your browser:

```text
http://127.0.0.1:8000
```

## How to Test

```bash
python -m unittest discover -s tests
```

## API

### `GET /tasks`

Returns all tasks.

Example response:

```json
{
  "success": true,
  "data": [
    {
      "id": "4ae8c2fc-6d51-44b2-aef4-c19f8b58b0f7",
      "title": "Prepare demo",
      "completed": false,
      "createdAt": "2026-04-09T19:25:00.000000+00:00"
    }
  ]
}
```

### `POST /tasks`

Creates a new task.

Request body:

```json
{
  "title": "Prepare demo"
}
```

### `PATCH /tasks/:id`

Updates a task's completion status.

Request body:

```json
{
  "completed": true
}
```

### `DELETE /tasks/:id`

Deletes a task by id.

## Validation Rules

- `title` is required for task creation
- `title` must be a non-empty string
- `title` must be 120 characters or fewer
- `completed` is required for updates
- `completed` must be a boolean

## Project Structure

```text
task-manager/
|-- app.py
|-- data/
|   `-- tasks.json
|-- static/
|   |-- app.js
|   |-- index.html
|   `-- styles.css
|-- task_manager/
|   |-- task_store.py
|   |-- validation.py
|   `-- __init__.py
`-- tests/
    `-- test_task_store.py
```

## Notes and Trade-offs

- I used file-based persistence instead of a database to keep the solution intentionally small for the assignment scope.
- I kept the frontend in vanilla JavaScript to avoid build tooling and make the code easy to inspect quickly.
- The `PATCH` endpoint only updates completion status because that is the required behavior from the assignment brief.
