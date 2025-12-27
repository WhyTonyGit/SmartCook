import pytest
from service import AuthService
from repository import ConsumerRepository
from exception import ValidationError, UnauthorizedError

def test_register_success(app):
    with app.app_context():
        consumer = AuthService.register('testuser', 'test@example.com', None, 'password123')
        assert consumer.username == 'testuser'
        assert consumer.email == 'test@example.com'

def test_register_duplicate_email(app):
    with app.app_context():
        AuthService.register('user1', 'test@example.com', None, 'password123')
        with pytest.raises(ValidationError):
            AuthService.register('user2', 'test@example.com', None, 'password123')

def test_login_success(app):
    with app.app_context():
        AuthService.register('testuser', 'test@example.com', None, 'password123')
        result = AuthService.login('test@example.com', 'password123')
        assert 'access_token' in result
        assert result['consumer']['email'] == 'test@example.com'

def test_login_wrong_password(app):
    with app.app_context():
        AuthService.register('testuser', 'test@example.com', None, 'password123')
        with pytest.raises(UnauthorizedError):
            AuthService.login('test@example.com', 'wrongpassword')

def test_generate_token(app):
    with app.app_context():
        consumer = AuthService.register('testuser', 'test@example.com', None, 'password123')
        token = AuthService.generate_token(consumer.id)
        assert token is not None
        
        consumer_id = AuthService.verify_token(token)
        assert consumer_id == consumer.id

