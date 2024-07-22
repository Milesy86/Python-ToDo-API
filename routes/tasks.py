from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.task import Task
from database import database

bp = Blueprint("tasks", __name__)

# Retrieve the list of all tasks (authentication required).
@bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    tasks = database.session.execute(database.select(Task)).scalars()
    return jsonify({"tasks": [task.to_dict() for task in tasks]}), 200

# Add a new task (authentication required).
@bp.route("/tasks", methods=["POST"])
@jwt_required()
def add_task():
    allowed_properties = ["title", "description", "completed", "user_id"]
    data = {key: value for key, value in request.get_json().items() if key in allowed_properties}
    if not "completed" in data:
        data["completed"] = False
    if len(data) != 4:
        return jsonify({"error": "Title, description and user_id are required."}), 400
    new_task = Task(title=data.get("title"), description=data.get("description"), completed=data.get("completed"), user_id=data.get("user_id"))
    database.session.add(new_task)
    database.session.commit()
    return jsonify({"msg": "Task added"}), 201
    
# Update an existing task (authentication required).
@bp.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    task = database.get_or_404(Task, task_id)
    data = request.get_json()
    # Replace fields in the task if they"ve been sent in the request, otherwise leave them alone
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.completed = data.get("completed", task.completed)
    task.user_id = data.get("user_id", task.user_id)
    database.session.commit()
    return jsonify({"msg": "Task updated"}), 200

# Remove a task (authentication required).
@bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    task = database.get_or_404(Task, task_id)
    database.session.delete(task)
    database.session.commit()
    return jsonify({"msg": "Task deleted"}), 201

# Retrieve a task by id (authentication required).
@bp.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task_by_id(task_id):
    task = database.get_or_404(Task, task_id)
    return jsonify(task.to_dict()), 200