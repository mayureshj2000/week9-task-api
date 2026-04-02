def validate_task_data(data: dict, update: bool = False):
    errors = {}

    if not update or "title" in data:
        title = data.get("title", "")
        if not title:
            errors.setdefault("title", []).append("Title is required")
        elif len(title) < 3:
            errors.setdefault("title", []).append("Title must be at least 3 characters")

    if "priority" in data:
        if data["priority"] not in ["low", "medium", "high"]:
            errors.setdefault("priority", []).append(
                "Priority must be one of: low, medium, high"
            )

    if "status" in data:
        if data["status"] not in ["pending", "in_progress", "completed"]:
            errors.setdefault("status", []).append(
                "Status must be one of: pending, in_progress, completed"
            )

    return {"valid": not errors, "errors": errors}