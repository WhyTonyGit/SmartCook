import jwt
from datetime import datetime, timedelta
from config import Config
from repository import ConsumerRepository
from exception import ValidationError, UnauthorizedError
from models import Consumer

class AuthService:
    @staticmethod
    def register(username, email, phone, password):
        # Валидация
        if not username or not email or not password:
            raise ValidationError("Username, email and password are required")
        
        if ConsumerRepository.get_by_email(email):
            raise ValidationError("Email already exists")
        
        if phone and ConsumerRepository.get_by_phone(phone):
            raise ValidationError("Phone already exists")
        
        consumer = ConsumerRepository.create(username, email, phone, password)
        return consumer
    
    @staticmethod
    def login(email_or_phone, password):
        if not email_or_phone or not password:
            raise ValidationError("Email/phone and password are required")
        
        consumer = ConsumerRepository.get_by_email_or_phone(email_or_phone)
        if not consumer or not consumer.check_password(password):
            raise UnauthorizedError("Invalid credentials")
        
        token = AuthService.generate_token(consumer.id)
        return {
            'access_token': token,
            'consumer': consumer.to_dict()
        }
    
    @staticmethod
    def generate_token(consumer_id):
        payload = {
            'consumer_id': consumer_id,
            'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    
    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
            return payload.get('consumer_id')
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Token expired")
        except jwt.InvalidTokenError:
            raise UnauthorizedError("Invalid token")
    
    @staticmethod
    def get_current_consumer(token):
        consumer_id = AuthService.verify_token(token)
        consumer = ConsumerRepository.get_by_id(consumer_id)
        if not consumer:
            raise UnauthorizedError("Consumer not found")
        return consumer

