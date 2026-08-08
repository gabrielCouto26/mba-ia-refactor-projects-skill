from flask import Blueprint, request, jsonify
from services.user_service import UserService
from services.task_service import TaskService
from schemas.user_schema import UserCreateSchema, UserUpdateSchema, UserLoginSchema
from schemas.task_schema import TaskCreateSchema, TaskUpdateSchema, TaskSearchSchema
from exceptions import ValidationError, NotFoundError, ConflictError, UnauthorizedError, ForbiddenError, APIError

user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    return jsonify(UserService.get_all_users()), 200

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify(UserService.get_user_by_id(user_id)), 200

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        raise ValidationError('Dados inválidos')
    try:
        validated = UserCreateSchema().load(data)
    except Exception as e:
        raise ValidationError(str(e))
    user = UserService.create_user(validated)
    return jsonify(user), 201

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        raise ValidationError('Dados inválidos')
    try:
        validated = UserUpdateSchema().load(data, partial=True)
    except Exception as e:
        raise ValidationError(str(e))
    user = UserService.update_user(user_id, validated)
    return jsonify(user), 200

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = UserService.delete_user(user_id)
    return jsonify(result), 200

@user_bp.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    # Reuse TaskService to fetch tasks for a user
    tasks = TaskService.search_tasks(user_id=user_id)
    return jsonify(tasks), 200

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        raise ValidationError('Dados inválidos')
    try:
        validated = UserLoginSchema().load(data)
    except Exception as e:
        raise ValidationError(str(e))
    auth = UserService.authenticate_user(validated['email'], validated['password'])
    return jsonify(auth), 200
