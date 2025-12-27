from flask import Blueprint, request, jsonify
from service import AuthService
from repository import ConsumerRepository
from api.middleware import require_auth
from exception import ValidationError

bp = Blueprint('auth', __name__)

@bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        raise ValidationError("Request body is required")
    
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    
    consumer = AuthService.register(username, email, phone, password)
    token = AuthService.generate_token(consumer.id)
    
    return jsonify({
        'access_token': token,
        'consumer': consumer.to_dict()
    }), 201

@bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        raise ValidationError("Request body is required")
    
    email_or_phone = data.get('emailOrPhone')
    password = data.get('password')
    
    result = AuthService.login(email_or_phone, password)
    return jsonify(result), 200

@bp.route('/me', methods=['GET'])
@require_auth
def get_profile():
    consumer = request.current_consumer
    return jsonify(consumer.to_dict()), 200

@bp.route('/me', methods=['PUT'])
@require_auth
def update_profile():
    data = request.get_json()
    consumer = request.current_consumer
    
    updates = {}
    if 'username' in data:
        updates['username'] = data['username']
    if 'avatar_url' in data:
        updates['avatar_url'] = data['avatar_url']
    
    updated = ConsumerRepository.update(consumer.id, **updates)
    return jsonify(updated.to_dict()), 200

@bp.route('/me/forbidden-ingredients', methods=['GET'])
@require_auth
def get_forbidden_ingredients():
    consumer = request.current_consumer
    ingredients = [ing.to_dict() for ing in consumer.forbidden_ingredients]
    return jsonify(ingredients), 200

@bp.route('/me/forbidden-ingredients', methods=['PUT'])
@require_auth
def update_forbidden_ingredients():
    data = request.get_json()
    consumer = request.current_consumer
    
    ingredient_ids = data.get('ingredient_ids', [])
    ConsumerRepository.set_forbidden_ingredients(consumer.id, ingredient_ids)
    
    updated = ConsumerRepository.get_by_id(consumer.id)
    ingredients = [ing.to_dict() for ing in updated.forbidden_ingredients]
    return jsonify(ingredients), 200

