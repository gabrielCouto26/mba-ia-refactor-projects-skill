from flask import Blueprint, request, jsonify
from services.task_service import TaskService
from schemas.task_schema import TaskCreateSchema, TaskUpdateSchema, TaskSearchSchema
from exceptions import ValidationError, NotFoundError, ConflictError, UnauthorizedError, ForbiddenError, APIError

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Retrieve all tasks."""
    tasks = TaskService.get_all_tasks()
    return jsonify(tasks), 200

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Retrieve a specific task by ID."""
    task = TaskService.get_task_by_id(task_id)
    return jsonify(task), 200

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data:
        raise ValidationError('Dados inválidos')
    try:
        validated = TaskCreateSchema().load(data)
    except Exception as e:
        raise ValidationError(str(e))
    task = TaskService.create_task(validated)
    return jsonify(task), 201

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    if not data:
        raise ValidationError('Dados inválidos')
    try:
        validated = TaskUpdateSchema().load(data, partial=True)
    except Exception as e:
        raise ValidationError(str(e))
    task = TaskService.update_task(task_id, validated)
    return jsonify(task), 200

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = TaskService.delete_task(task_id)
    return jsonify(result), 200

@task_bp.route('/tasks/search', methods=['GET'])
def search_tasks():
    try:
        validated = TaskSearchSchema().load(request.args)
    except Exception as e:
        raise ValidationError(str(e))
    tasks = TaskService.search_tasks(**validated)
    return jsonify(tasks), 200

@task_bp.route('/tasks/stats', methods=['GET'])
def task_stats():
    stats = TaskService.get_task_stats()
    return jsonify(stats), 200
