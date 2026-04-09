"""Validation helpers for task payloads."""


def validate_task_title(payload):
    if not isinstance(payload, dict):
        return "Request body must be a JSON object."

    title = payload.get("title")
    if not isinstance(title, str):
        return "Field 'title' is required and must be a string."

    normalized_title = title.strip()
    if not normalized_title:
        return "Field 'title' cannot be empty."

    if len(normalized_title) > 120:
        return "Field 'title' must be 120 characters or fewer."

    return None


def validate_task_update(payload):
    if not isinstance(payload, dict):
        return "Request body must be a JSON object."

    allowed_keys = {"completed"}
    unexpected_keys = set(payload.keys()) - allowed_keys
    if unexpected_keys:
        return "Only the 'completed' field can be updated."

    if "completed" not in payload:
        return "Field 'completed' is required."

    if not isinstance(payload["completed"], bool):
        return "Field 'completed' must be a boolean."

    return None
