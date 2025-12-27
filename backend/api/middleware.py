from flask import request, jsonify
from service import AuthService
from exception import UnauthorizedError, ForbiddenError

def require_auth(f):
    """Декоратор для проверки авторизации"""
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            raise UnauthorizedError("Authorization token required")
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        try:
            consumer = AuthService.get_current_consumer(token)
            request.current_consumer = consumer
            return f(*args, **kwargs)
        except Exception as e:
            raise UnauthorizedError(str(e))
    
    wrapper.__name__ = f.__name__
    return wrapper

def require_admin(f):
    """Декоратор для проверки прав администратора"""
    def wrapper(*args, **kwargs):
        if not hasattr(request, 'current_consumer'):
            raise UnauthorizedError("Authentication required")
        
        if request.current_consumer.role_id != 1:
            raise ForbiddenError("Admin access required")
        
        return f(*args, **kwargs)
    
    wrapper.__name__ = f.__name__
    return wrapper

