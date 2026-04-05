from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.tasks import bp
from app.extensions import db, limiter
from app.models import Task
from app.utils.validators import validate_task_data
from app.utils.responses import success_response, error_response

print("HEADERS:", dict(request.headers))

def serialize_task(task: Task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }

@bp.get("")
@jwt_required()
@limiter.limit("60 per minute")
def list_tasks():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    status = request.args.get("status")
    priority = request.args.get("priority")
    sort_by = request.args.get("sort_by", "created_at")
    sort_order = request.args.get("sort_order", "desc")

    query = Task.query.filter_by(user_id=user_id)

    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)

    if hasattr(Task, sort_by):
        column = getattr(Task, sort_by)
        query = query.order_by(column.desc() if sort_order == "desc" else column.asc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return success_response(
        {
            "tasks": [serialize_task(t) for t in pagination.items],
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total_pages": pagination.pages,
                "total_items": pagination.total,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
            },
        }
    )

@bp.post("")
@jwt_required()
@limiter.limit("30 per minute")
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    result = validate_task_data(data)
    if not result["valid"]:
        return error_response("Validation failed", 400, result["errors"])

    task = Task(
        title=data["title"],
        description=data.get("description", ""),
        status=data.get("status", "pending"),
        priority=data.get("priority", "medium"),
        user_id=user_id,
    )
    db.session.add(task)
    db.session.commit()

    return success_response(
        {"message": "Task created successfully", "task": serialize_task(task)}, 201
    )

@bp.get("/<int:task_id>")
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return error_response("Task not found", 404)
    return success_response({"task": serialize_task(task)})

@bp.put("/<int:task_id>")
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return error_response("Task not found", 404)

    result = validate_task_data(data, update=True)
    if not result["valid"]:
        return error_response("Validation failed", 400, result["errors"])

    for field in ["title", "description", "status", "priority"]:
        if field in data:
            setattr(task, field, data[field])

    db.session.commit()
    return success_response(
        {"message": "Task updated successfully", "task": serialize_task(task)}
    )

@bp.delete("/<int:task_id>")
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return error_response("Task not found", 404)
    db.session.delete(task)
    db.session.commit()
    # 204 usually has no body, but sample uses a message
    return success_response({"message": "Task deleted successfully"}, 204)