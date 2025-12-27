from flask import Blueprint, request, jsonify
from service import RecipeService, IngredientService
from repository import RecipeRepository, ConsumerRepository
from api.middleware import require_auth
from exception import ValidationError, NotFoundError
from models import Mark, Comment

bp = Blueprint('recipes', __name__)

@bp.route('/recipes', methods=['GET'])
def search_recipes():
    # Получаем параметры запроса
    query = request.args.get('q')
    ingredients_param = request.args.get('ingredients')
    min_match = float(request.args.get('minMatch', 0.0))
    max_time = request.args.get('maxTime', type=int)
    difficulty = request.args.get('difficulty')
    category_id = request.args.get('categoryId', type=int)
    sort = request.args.get('sort', 'match')
    
    # Получаем запрещённые ингредиенты пользователя, если авторизован
    forbidden_ingredient_ids = None
    user_ingredient_ids = None
    
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        try:
            from service import AuthService
            consumer = AuthService.get_current_consumer(token[7:])
            forbidden_ingredient_ids = [ing.id for ing in consumer.forbidden_ingredients]
        except:
            pass
    
    # Разрешаем ингредиенты
    if ingredients_param:
        ingredient_list = [i.strip() for i in ingredients_param.split(',') if i.strip()]
        user_ingredient_ids = IngredientService.resolve_ingredient_ids(ingredient_list)
    
    # Поиск рецептов
    results = RecipeService.search_recipes(
        user_ingredient_ids=user_ingredient_ids,
        forbidden_ingredient_ids=forbidden_ingredient_ids,
        query=query,
        max_time=max_time,
        difficulty=difficulty,
        category_id=category_id,
        min_match=min_match,
        sort=sort
    )
    
    return jsonify(results), 200

@bp.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    # Получаем ингредиенты пользователя, если авторизован
    user_ingredient_ids = None
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        try:
            from service import AuthService
            consumer = AuthService.get_current_consumer(token[7:])
            # Можно использовать ингредиенты из профиля или передавать отдельно
        except:
            pass
    
    recipe = RecipeService.get_recipe(recipe_id, user_ingredient_ids)
    return jsonify(recipe), 200

@bp.route('/recipes/<int:recipe_id>/missing', methods=['GET'])
def get_missing_ingredients(recipe_id):
    ingredients_param = request.args.get('ingredients', '')
    if not ingredients_param:
        raise ValidationError("ingredients parameter is required")
    
    ingredient_list = [i.strip() for i in ingredients_param.split(',') if i.strip()]
    ingredient_ids = IngredientService.resolve_ingredient_ids(ingredient_list)
    
    missing = RecipeRepository.get_missing_ingredients(recipe_id, ingredient_ids)
    return jsonify([ing.to_dict() for ing in missing]), 200

@bp.route('/favourites', methods=['GET'])
@require_auth
def get_favorites():
    consumer = request.current_consumer
    recipes = RecipeRepository.get_favorites(consumer.id)
    results = []
    for recipe in recipes:
        recipe_dict = recipe.to_dict()
        marks = Mark.query.filter_by(recipe_id=recipe.id).all()
        recipe_dict['avg_rating'] = sum(m.value for m in marks) / len(marks) if marks else 0.0
        recipe_dict['comments_count'] = Comment.query.filter_by(recipe_id=recipe.id).count()
        recipe_dict['categories'] = [c.to_dict() for c in recipe.categories]
        results.append(recipe_dict)
    return jsonify(results), 200

@bp.route('/favourites', methods=['POST'])
@require_auth
def add_favorite():
    data = request.get_json()
    recipe_id = data.get('recipe_id')
    if not recipe_id:
        raise ValidationError("recipe_id is required")
    
    consumer = request.current_consumer
    RecipeRepository.add_to_favorites(consumer.id, recipe_id)
    return jsonify({'message': 'Added to favorites'}), 201

@bp.route('/favourites/<int:recipe_id>', methods=['DELETE'])
@require_auth
def remove_favorite(recipe_id):
    consumer = request.current_consumer
    RecipeRepository.remove_from_favorites(consumer.id, recipe_id)
    return jsonify({'message': 'Removed from favorites'}), 200

@bp.route('/history', methods=['GET'])
@require_auth
def get_history():
    consumer = request.current_consumer
    recipes = RecipeRepository.get_history(consumer.id)
    results = []
    for recipe in recipes:
        recipe_dict = recipe.to_dict()
        marks = Mark.query.filter_by(recipe_id=recipe.id).all()
        recipe_dict['avg_rating'] = sum(m.value for m in marks) / len(marks) if marks else 0.0
        recipe_dict['comments_count'] = Comment.query.filter_by(recipe_id=recipe.id).count()
        recipe_dict['categories'] = [c.to_dict() for c in recipe.categories]
        results.append(recipe_dict)
    return jsonify(results), 200

@bp.route('/history', methods=['POST'])
@require_auth
def add_to_history():
    data = request.get_json()
    recipe_id = data.get('recipe_id')
    if not recipe_id:
        raise ValidationError("recipe_id is required")
    
    consumer = request.current_consumer
    RecipeRepository.add_to_history(consumer.id, recipe_id)
    return jsonify({'message': 'Added to history'}), 201

@bp.route('/recommendations', methods=['GET'])
@require_auth
def get_recommendations():
    consumer = request.current_consumer
    recipes = RecipeService.get_recommendations(consumer.id)
    return jsonify(recipes), 200

