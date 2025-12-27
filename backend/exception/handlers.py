from flask import jsonify
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

class AppException(Exception):
    def __init__(self, message, code=400, details=None):
        self.message = message
        self.code = code
        self.details = details
        super().__init__(self.message)

class ValidationError(AppException):
    pass

class NotFoundError(AppException):
    def __init__(self, message="Resource not found", details=None):
        super().__init__(message, code=404, details=details)

class UnauthorizedError(AppException):
    def __init__(self, message="Unauthorized", details=None):
        super().__init__(message, code=401, details=details)

class ForbiddenError(AppException):
    def __init__(self, message="Forbidden", details=None):
        super().__init__(message, code=403, details=details)

def register_error_handlers(app):
    @app.errorhandler(AppException)
    def handle_app_exception(e):
        response = {
            'error': {
                'code': e.code,
                'message': e.message
            }
        }
        if e.details:
            response['error']['details'] = e.details
        return jsonify(response), e.code
    
    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        return jsonify({
            'error': {
                'code': 400,
                'message': str(e.description) if e.description else 'Bad request'
            }
        }), 400
    
    @app.errorhandler(NotFound)
    def handle_not_found(e):
        return jsonify({
            'error': {
                'code': 404,
                'message': 'Resource not found'
            }
        }), 404
    
    @app.errorhandler(Unauthorized)
    def handle_unauthorized(e):
        return jsonify({
            'error': {
                'code': 401,
                'message': 'Unauthorized'
            }
        }), 401
    
    @app.errorhandler(Forbidden)
    def handle_forbidden(e):
        return jsonify({
            'error': {
                'code': 403,
                'message': 'Forbidden'
            }
        }), 403
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        return jsonify({
            'error': {
                'code': 500,
                'message': 'Internal server error'
            }
        }), 500

