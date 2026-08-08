from flask import jsonify
from validators.product_validator import ValidationError

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        response = jsonify({"erro": error.message, "sucesso": False})
        return response, error.status_code

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"erro": "Recurso não encontrado", "sucesso": False}), 404

    @app.errorhandler(400)
    def handle_bad_request(error):
        return jsonify({"erro": "Requisição inválida", "sucesso": False}), 400

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        # Log error in production environment
        app.logger.error(f"Unhandled Exception: {str(error)}")
        return jsonify({"erro": str(error)}), 500
