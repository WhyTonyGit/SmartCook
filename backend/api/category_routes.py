from flask import Blueprint, jsonify
from service import CategoryService

bp = Blueprint('categories', __name__)

@bp.route('/categories', methods=['GET'])
def get_categories():
    categories = CategoryService.get_all()
    return jsonify([c.to_dict() for c in categories]), 200

