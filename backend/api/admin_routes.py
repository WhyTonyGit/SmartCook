from flask import Blueprint, request, jsonify
from repository import RecipeRepository, CommentRepository, CategoryRepository, IngredientRepository
from api.middleware import require_auth, require_admin
from exception import ValidationError, NotFoundError

bp = Blueprint('admin', __name__)

@bp.route('/admin/recipes', methods=['GET'])
@require_auth
@require_admin
def list_recipes():
    recipes = RecipeRepository.get_all()
    return jsonify([r.to_dict() for r in recipes]), 200

@bp.route('/admin/recipes', methods=['POST'])
@require_auth
@require_admin
def create_recipe():
    data = request.get_json()
    if not data:
        raise ValidationError("Request body is required")
    
    recipe = RecipeRepository.create(
        title=data.get('title'),
        description=data.get('description'),
        cooking_time=data.get('cooking_time'),
        difficulty=data.get('difficulty', 'medium'),
        image_url=data.get('image_url'),
        category_ids=data.get('category_ids'),
        ingredient_ids=data.get('ingredient_ids')
    )
    return jsonify(recipe.to_dict(include_details=True)), 201

@bp.route('/admin/recipes/<int:recipe_id>', methods=['PUT'])
@require_auth
@require_admin
def update_recipe(recipe_id):
    data = request.get_json()
    if not data:
        raise ValidationError("Request body is required")
    
    updates = {}
    for key in ['title', 'description', 'cooking_time', 'difficulty', 'image_url']:
        if key in data:
            updates[key] = data[key]
    
    recipe = RecipeRepository.update(recipe_id, **updates)
    return jsonify(recipe.to_dict(include_details=True)), 200

@bp.route('/admin/recipes/<int:recipe_id>', methods=['DELETE'])
@require_auth
@require_admin
def delete_recipe(recipe_id):
    RecipeRepository.delete(recipe_id)
    return jsonify({'message': 'Recipe deleted'}), 200

@bp.route('/admin/comments/<int:comment_id>', methods=['DELETE'])
@require_auth
@require_admin
def delete_comment(comment_id):
    CommentRepository.delete(comment_id)
    return jsonify({'message': 'Comment deleted'}), 200

@bp.route('/admin/categories', methods=['POST'])
@require_auth
@require_admin
def create_category():
    data = request.get_json()
    name = data.get('name')
    if not name:
        raise ValidationError("name is required")
    
    category = CategoryRepository.create(name)
    return jsonify(category.to_dict()), 201

@bp.route('/admin/ingredients', methods=['POST'])
@require_auth
@require_admin
def create_ingredient():
    data = request.get_json()
    name = data.get('name')
    if not name:
        raise ValidationError("name is required")
    
    ingredient = IngredientRepository.create(
        name=name,
        image_url=data.get('image_url')
    )
    return jsonify(ingredient.to_dict()), 201

