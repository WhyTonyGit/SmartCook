from flask import Blueprint, request, jsonify
from service import MarkService
from api.middleware import require_auth
from exception import ValidationError

bp = Blueprint('marks', __name__)

@bp.route('/recipes/<int:recipe_id>/mark', methods=['POST'])
@require_auth
def upsert_mark(recipe_id):
    data = request.get_json()
    value = data.get('value')
    if not value:
        raise ValidationError("value is required")
    
    consumer = request.current_consumer
    mark = MarkService.upsert_mark(recipe_id, consumer.id, value)
    return jsonify(mark.to_dict()), 200

@bp.route('/me/marks', methods=['GET'])
@require_auth
def get_marks():
    consumer = request.current_consumer
    marks = MarkService.get_marks(consumer.id)
    return jsonify([m.to_dict() for m in marks]), 200

@bp.route('/recipes/<int:recipe_id>/mark', methods=['DELETE'])
@require_auth
def delete_mark(recipe_id):
    consumer = request.current_consumer
    deleted = MarkService.delete_mark(recipe_id, consumer.id)
    return jsonify({'deleted': deleted}), 200
