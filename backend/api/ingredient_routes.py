from flask import Blueprint, request, jsonify
from service import IngredientService

bp = Blueprint('ingredients', __name__)

@bp.route('/ingredients', methods=['GET'])
def get_ingredients():
    query = request.args.get('q')
    limit = request.args.get('limit', 100, type=int)
    
    ingredients = IngredientService.search_ingredients(query=query, limit=limit)
    return jsonify([ing.to_dict() for ing in ingredients]), 200

