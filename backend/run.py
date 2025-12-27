from flask import Flask
from config import Config
from extensions import db, migrate, cors
from api.routes import register_routes
from exception.handlers import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])
    
    register_routes(app)
    register_error_handlers(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

