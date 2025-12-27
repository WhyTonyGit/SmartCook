from flask import Blueprint, request, jsonify
from api import auth_routes, recipe_routes, ingredient_routes, category_routes, comment_routes, mark_routes, admin_routes

def register_routes(app):
    api = Blueprint('api', __name__, url_prefix='/api')
    
    api.register_blueprint(auth_routes.bp)
    api.register_blueprint(recipe_routes.bp)
    api.register_blueprint(ingredient_routes.bp)
    api.register_blueprint(category_routes.bp)
    api.register_blueprint(comment_routes.bp)
    api.register_blueprint(mark_routes.bp)
    api.register_blueprint(admin_routes.bp)
    
    app.register_blueprint(api)

