import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://smartcook:smartcook_pass@localhost:5432/smartcook_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = 24
    
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:8080').split(',')

