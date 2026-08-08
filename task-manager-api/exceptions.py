class APIError(Exception):
    def __init__(self, message, status_code=400, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv

class NotFoundError(APIError):
    def __init__(self, message='Recurso não encontrado'):
        super().__init__(message, status_code=404)

class ConflictError(APIError):
    def __init__(self, message='Recurso já existente'):
        super().__init__(message, status_code=409)

class UnauthorizedError(APIError):
    def __init__(self, message='Credenciais inválidas'):
        super().__init__(message, status_code=401)

class ForbiddenError(APIError):
    def __init__(self, message='Acesso negado'):
        super().__init__(message, status_code=403)

class ValidationError(APIError):
    def __init__(self, message='Dados inválidos'):
        super().__init__(message, status_code=400)
