# Task Manager

A small full stack Task Manager built for the technical assignment. The project uses Python's standard library for the backend and a simple vanilla JavaScript frontend, so it runs without installing extra packages.

## Features

- View all tasks
- Add a new task
- Mark a task as completed or active
- Delete a task
- Show loading, success, and error states
- Persist tasks after refresh using a local JSON file
- Filter tasks by all, active, or completed

## Project Structure

```text
task-manager/
|-- app.py
|-- data/
|-- static/
|   |-- app.js
|   |-- index.html
|   `-- styles.css
|-- task_manager/
|   |-- task_store.py
|   `-- validation.py
`-- tests/
    `-- test_task_store.py
```

## Run Locally

1. Open a terminal in `task-manager`.
2. Start the server:

```bash
python app.py
```

3. Open `http://127.0.0.1:8000` in your browser.

## Run Tests

```bash
python -m unittest discover -s tests
```

## API Endpoints

- `GET /tasks` returns all tasks
- `POST /tasks` creates a task with a `title`
- `PATCH /tasks/:id` updates the `completed` status
- `DELETE /tasks/:id` deletes a task

## Example Payloads

Create a task:

```json
{
  "title": "Prepare demo"
}
```

Update a task:

```json
{
  "completed": true
}
```

## Assumptions and Trade-offs

- I used file-based storage instead of a database to keep the app intentionally small.
- The backend only supports updating task completion status because that is the required PATCH behavior in the assignment.
- The frontend is plain JavaScript to avoid setup overhead and keep the app easy to review.
