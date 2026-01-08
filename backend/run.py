from flask import Flask, request
from config import Config
from extensions import db, migrate, cors
from api.routes import register_routes
from exception.handlers import register_error_handlers
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Инициализируем CORS с полной конфигурацией для всех /api/* маршрутов
    # Важно: CORS должен быть инициализирован ДО регистрации routes
    cors.init_app(
        app,
        resources={r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": False,
            "expose_headers": ["Content-Type"]
        }},
        automatic_options=True  # Автоматически обрабатывать OPTIONS
    )
    
    # Логирование всех запросов к /api/*
    @app.before_request
    def log_request_info():
        if request.path.startswith('/api/'):
            logger.info(f"{request.method} {request.path} - Origin: {request.headers.get('Origin', 'N/A')}")
    
    @app.after_request
    def log_response_info(response):
        if request.path.startswith('/api/'):
            logger.info(f"{request.method} {request.path} - Status: {response.status_code}")
        return response
    
    register_routes(app)
    register_error_handlers(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

