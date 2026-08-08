from flask import Blueprint, request, jsonify
from services.report_service import ReportService
from schemas.category_schema import CategoryCreateSchema, CategoryUpdateSchema
from exceptions import ValidationError, NotFoundError, APIError

report_bp = Blueprint('reports', __name__)

@report_bp.route('/reports/summary', methods=['GET'])
def summary_report():
    """Generate an overview summary of the system."""
    report = ReportService.summary_report()
    return jsonify(report), 200

@report_bp.route('/reports/user/<int:user_id>', methods=['GET'])
def user_report(user_id):
    """Generate a productivity report for a specific user."""
    report = ReportService.user_report(user_id)
    return jsonify(report), 200

@report_bp.route('/categories', methods=['GET'])
def get_categories():
    """List all categories with task counts."""
    categories = ReportService.list_categories()
    return jsonify(categories), 200

@report_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data:
        raise ValidationError('Dados inválidos')
    try:
        validated = CategoryCreateSchema().load(data)
    except Exception as e:
        raise ValidationError(str(e))
    category = ReportService.create_category(validated)
    return jsonify(category), 201

@report_bp.route('/categories/<int:cat_id>', methods=['PUT'])
def update_category(cat_id):
    data = request.get_json()
    if not data:
        raise ValidationError('Dados inválidos')
    try:
        validated = CategoryUpdateSchema().load(data, partial=True)
    except Exception as e:
        raise ValidationError(str(e))
    category = ReportService.update_category(cat_id, validated)
    return jsonify(category), 200

@report_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    result = ReportService.delete_category(cat_id)
    return jsonify(result), 200
