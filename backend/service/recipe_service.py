from repository import RecipeRepository, ConsumerRepository, IngredientRepository
from exception import NotFoundError, ValidationError
from sqlalchemy import func
from models import Mark, Comment

class RecipeService:
    @staticmethod
    def search_recipes(
        user_ingredient_ids=None,
        forbidden_ingredient_ids=None,
        query=None,
        max_time=None,
        difficulty=None,
        category_id=None,
        min_match=0.0,
        sort='match'
    ):
        # Получаем базовый список рецептов
        recipes = RecipeRepository.search(
            query=query,
            ingredient_ids=None,  # Вычисляем match в сервисе
            forbidden_ingredient_ids=forbidden_ingredient_ids,
            max_time=max_time,
            difficulty=difficulty,
            category_id=category_id,
            min_match=0.0,
            sort=sort
        )
        
        # Если есть ингредиенты для поиска, вычисляем match_percent
        if user_ingredient_ids:
            results = []
            for recipe in recipes:
                match_info = RecipeRepository.calculate_match_info(recipe, user_ingredient_ids)
                if match_info['match_percent'] >= min_match:
                    recipe_dict = recipe.to_dict()
                    recipe_dict['match_percent'] = match_info['match_percent']
                    recipe_dict['missing_ingredients'] = match_info['missing_ingredients']
                    
                    # Добавляем статистику
                    recipe_dict['avg_rating'] = RecipeService._calculate_avg_rating(recipe.id)
                    recipe_dict['comments_count'] = RecipeService._count_comments(recipe.id)
                    recipe_dict['categories'] = [c.to_dict() for c in recipe.categories]
                    
                    results.append(recipe_dict)
            
            # Сортировка
            if sort == 'match':
                results.sort(key=lambda x: x['match_percent'], reverse=True)
            elif sort == 'rating':
                results.sort(key=lambda x: (x['avg_rating'], x['match_percent']), reverse=True)
            elif sort == 'time':
                results.sort(key=lambda x: (x['cooking_time'], -x['match_percent']))
            elif sort == 'popular':
                # Для popular нужно считать fav_count, упростим
                results.sort(key=lambda x: (x['comments_count'], x['match_percent']), reverse=True)
            
            return results
        else:
            # Без ингредиентов - просто возвращаем рецепты
            results = []
            for recipe in recipes:
                recipe_dict = recipe.to_dict()
                recipe_dict['match_percent'] = None
                recipe_dict['missing_ingredients'] = []
                recipe_dict['avg_rating'] = RecipeService._calculate_avg_rating(recipe.id)
                recipe_dict['comments_count'] = RecipeService._count_comments(recipe.id)
                recipe_dict['categories'] = [c.to_dict() for c in recipe.categories]
                results.append(recipe_dict)
            
            return results
    
    @staticmethod
    def _calculate_avg_rating(recipe_id):
        marks = Mark.query.filter_by(recipe_id=recipe_id).all()
        if marks:
            return sum(m.value for m in marks) / len(marks)
        return 0.0
    
    @staticmethod
    def _count_comments(recipe_id):
        return Comment.query.filter_by(recipe_id=recipe_id).count()
    
    @staticmethod
    def get_recipe(recipe_id, user_ingredient_ids=None):
        recipe = RecipeRepository.get_by_id(recipe_id)
        if not recipe:
            raise NotFoundError("Recipe not found")
        
        recipe_dict = recipe.to_dict(include_details=True)
        
        if user_ingredient_ids:
            match_info = RecipeRepository.calculate_match_info(recipe, user_ingredient_ids)
            recipe_dict['match_percent'] = match_info['match_percent']
            recipe_dict['missing_ingredients'] = match_info['missing_ingredients']
        else:
            recipe_dict['match_percent'] = None
            recipe_dict['missing_ingredients'] = []
        
        return recipe_dict
    
    @staticmethod
    def get_recommendations(consumer_id):
        consumer = ConsumerRepository.get_by_id(consumer_id)
        if not consumer:
            raise NotFoundError("Consumer not found")
        
        # Получаем историю
        history = RecipeRepository.get_history(consumer_id)
        
        if history:
            # Берём категории и ингредиенты из истории
            category_ids = set()
            ingredient_ids = set()
            for recipe in history[:5]:  # Берём последние 5
                category_ids.update(c.id for c in recipe.categories)
                ingredient_ids.update(ing.id for ing in recipe.ingredients)
            
            # Ищем рецепты с похожими категориями/ингредиентами
            forbidden_ids = [ing.id for ing in consumer.forbidden_ingredients]
            recipes = RecipeRepository.search(
                ingredient_ids=list(ingredient_ids) if ingredient_ids else None,
                forbidden_ingredient_ids=forbidden_ids,
                category_id=list(category_ids)[0] if category_ids else None,
                sort='popular'
            )
            
            # Исключаем уже просмотренные
            history_ids = {r.id for r in history}
            recipes = [r for r in recipes if r.id not in history_ids]
        else:
            # Топ популярных
            forbidden_ids = [ing.id for ing in consumer.forbidden_ingredients]
            recipes = RecipeRepository.search(
                forbidden_ingredient_ids=forbidden_ids,
                sort='popular'
            )
        
        results = []
        for recipe in recipes[:10]:  # Ограничиваем 10
            recipe_dict = recipe.to_dict()
            recipe_dict['avg_rating'] = RecipeService._calculate_avg_rating(recipe.id)
            recipe_dict['comments_count'] = RecipeService._count_comments(recipe.id)
            recipe_dict['categories'] = [c.to_dict() for c in recipe.categories]
            results.append(recipe_dict)
        
        return results

