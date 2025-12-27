from flask import Blueprint, request, jsonify
from service import CommentService
from api.middleware import require_auth
from exception import ValidationError

bp = Blueprint('comments', __name__)

@bp.route('/recipes/<int:recipe_id>/comments', methods=['GET'])
def get_comments(recipe_id):
    comments = CommentService.get_comments(recipe_id)
    return jsonify([c.to_dict() for c in comments]), 200

@bp.route('/recipes/<int:recipe_id>/comments', methods=['POST'])
@require_auth
def create_comment(recipe_id):
    data = request.get_json()
    text = data.get('text')
    if not text:
        raise ValidationError("text is required")
    
    consumer = request.current_consumer
    comment = CommentService.create_comment(recipe_id, consumer.id, text)
    return jsonify(comment.to_dict()), 201

@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@require_auth
def delete_comment(comment_id):
    consumer = request.current_consumer
    is_admin = consumer.role_id == 1
    CommentService.delete_comment(comment_id, consumer.id, is_admin)
    return jsonify({'message': 'Comment deleted'}), 200

