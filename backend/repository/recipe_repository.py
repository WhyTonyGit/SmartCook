from extensions import db
from models import Recipe, Difficulty, Mark
from models.associations import recipe_ingredient, consumer_recipe_fav, consumer_recipe_history
from sqlalchemy import func, desc, asc, and_, or_
from exception import NotFoundError

class RecipeRepository:
    @staticmethod
    def get_by_id(recipe_id):
        return Recipe.query.get(recipe_id)
    
    @staticmethod
    def get_all():
        return Recipe.query.all()
    
    @staticmethod
    def search(
        query=None,
        ingredient_ids=None,
        forbidden_ingredient_ids=None,
        max_time=None,
        difficulty=None,
        category_id=None,
        min_match=0.0,
        sort='match'
    ):
        q = Recipe.query
        
        # Исключаем рецепты с запрещёнными ингредиентами
        if forbidden_ingredient_ids:
            subquery = db.session.query(recipe_ingredient.c.recipe_id).filter(
                recipe_ingredient.c.ingredient_id.in_(forbidden_ingredient_ids)
            ).subquery()
            q = q.filter(~Recipe.id.in_(db.session.query(subquery.c.recipe_id)))
        
        # Поиск по названию
        if query:
            q = q.filter(Recipe.title.ilike(f'%{query}%'))
        
        # Фильтр по времени
        if max_time:
            q = q.filter(Recipe.cooking_time <= max_time)
        
        # Фильтр по сложности
        if difficulty:
            try:
                diff_enum = Difficulty[difficulty.upper()]
                q = q.filter(Recipe.difficulty == diff_enum)
            except KeyError:
                pass
        
        # Фильтр по категории
        if category_id:
            q = q.join(Recipe.categories).filter_by(id=category_id)
        
        # Сортировка
        if sort == 'rating':
            q = q.outerjoin(Mark).group_by(Recipe.id).order_by(desc(func.avg(Mark.value)))
        elif sort == 'time':
            q = q.order_by(asc(Recipe.cooking_time))
        elif sort == 'popular':
            q = q.outerjoin(consumer_recipe_fav).group_by(Recipe.id).order_by(desc(func.count(consumer_recipe_fav.c.consumer_id)))
        else:
            q = q.order_by(desc(Recipe.id))
        
        return q.all()
    
    @staticmethod
    def create(title, description, cooking_time, difficulty, image_url=None, category_ids=None, ingredient_ids=None):
        recipe = Recipe(
            title=title,
            description=description,
            cooking_time=cooking_time,
            difficulty=Difficulty[difficulty.upper()] if isinstance(difficulty, str) else difficulty,
            image_url=image_url
        )
        
        if category_ids:
            from models import Category
            categories = Category.query.filter(Category.id.in_(category_ids)).all()
            recipe.categories = categories
        
        if ingredient_ids:
            from models import Ingredient
            ingredients = Ingredient.query.filter(Ingredient.id.in_(ingredient_ids)).all()
            recipe.ingredients = ingredients
        
        db.session.add(recipe)
        db.session.commit()
        return recipe
    
    @staticmethod
    def update(recipe_id, **kwargs):
        recipe = RecipeRepository.get_by_id(recipe_id)
        if not recipe:
            raise NotFoundError("Recipe not found")
        
        if 'difficulty' in kwargs and isinstance(kwargs['difficulty'], str):
            kwargs['difficulty'] = Difficulty[kwargs['difficulty'].upper()]
        
        for key, value in kwargs.items():
            if hasattr(recipe, key) and value is not None:
                setattr(recipe, key, value)
        
        db.session.commit()
        return recipe
    
    @staticmethod
    def delete(recipe_id):
        recipe = RecipeRepository.get_by_id(recipe_id)
        if not recipe:
            raise NotFoundError("Recipe not found")
        db.session.delete(recipe)
        db.session.commit()
    
    @staticmethod
    def get_favorites(consumer_id):
        from models import Consumer
        consumer = Consumer.query.get(consumer_id)
        if not consumer:
            raise NotFoundError("Consumer not found")
        return consumer.favorite_recipes
    
    @staticmethod
    def add_to_favorites(consumer_id, recipe_id):
        from models import Consumer
        consumer = Consumer.query.get(consumer_id)
        recipe = RecipeRepository.get_by_id(recipe_id)
        if not consumer or not recipe:
            raise NotFoundError("Consumer or recipe not found")
        if recipe not in consumer.favorite_recipes:
            consumer.favorite_recipes.append(recipe)
            db.session.commit()
    
    @staticmethod
    def remove_from_favorites(consumer_id, recipe_id):
        from models import Consumer
        consumer = Consumer.query.get(consumer_id)
        recipe = RecipeRepository.get_by_id(recipe_id)
        if not consumer or not recipe:
            raise NotFoundError("Consumer or recipe not found")
        if recipe in consumer.favorite_recipes:
            consumer.favorite_recipes.remove(recipe)
            db.session.commit()
    
    @staticmethod
    def add_to_history(consumer_id, recipe_id):
        from models import Consumer, consumer_recipe_history
        from datetime import datetime
        consumer = Consumer.query.get(consumer_id)
        recipe = RecipeRepository.get_by_id(recipe_id)
        if not consumer or not recipe:
            raise NotFoundError("Consumer or recipe not found")
        
        # Проверяем, есть ли уже запись
        existing = db.session.query(consumer_recipe_history).filter(
            and_(
                consumer_recipe_history.c.consumer_id == consumer_id,
                consumer_recipe_history.c.recipe_id == recipe_id
            )
        ).first()
        
        if existing:
            # Обновляем viewed_at
            db.session.execute(
                consumer_recipe_history.update().where(
                    and_(
                        consumer_recipe_history.c.consumer_id == consumer_id,
                        consumer_recipe_history.c.recipe_id == recipe_id
                    )
                ).values(viewed_at=datetime.utcnow())
            )
        else:
            # Добавляем новую запись
            db.session.execute(
                consumer_recipe_history.insert().values(
                    consumer_id=consumer_id,
                    recipe_id=recipe_id,
                    viewed_at=datetime.utcnow()
                )
            )
        db.session.commit()
    
    @staticmethod
    def get_history(consumer_id):
        from models import Consumer, consumer_recipe_history
        from sqlalchemy import desc
        consumer = Consumer.query.get(consumer_id)
        if not consumer:
            raise NotFoundError("Consumer not found")
        
        # Получаем рецепты из истории с сортировкой по viewed_at
        history_records = db.session.query(
            consumer_recipe_history.c.recipe_id,
            consumer_recipe_history.c.viewed_at
        ).filter_by(consumer_id=consumer_id).order_by(
            desc(consumer_recipe_history.c.viewed_at)
        ).all()
        
        recipe_ids = [r.recipe_id for r in history_records]
        recipes = Recipe.query.filter(Recipe.id.in_(recipe_ids)).all()
        
        # Сохраняем порядок
        recipe_dict = {r.id: r for r in recipes}
        return [recipe_dict[rid] for rid in recipe_ids if rid in recipe_dict]
    
    @staticmethod
    def get_missing_ingredients(recipe_id, ingredient_ids):
        recipe = RecipeRepository.get_by_id(recipe_id)
        if not recipe:
            raise NotFoundError("Recipe not found")
        
        recipe_ingredient_ids = {ing.id for ing in recipe.ingredients}
        user_ingredient_ids = set(ingredient_ids)
        missing_ids = recipe_ingredient_ids - user_ingredient_ids
        
        from models import Ingredient
        return Ingredient.query.filter(Ingredient.id.in_(missing_ids)).all()
    
    @staticmethod
    def calculate_match_info(recipe, ingredient_ids):
        """Вычисляет match_percent и missing ingredients для рецепта"""
        recipe_ingredient_ids = {ing.id for ing in recipe.ingredients}
        user_ingredient_ids = set(ingredient_ids)
        
        total = len(recipe_ingredient_ids)
        matched = len(recipe_ingredient_ids & user_ingredient_ids)
        match_percent = (matched / total) if total > 0 else 0.0
        
        missing_ids = recipe_ingredient_ids - user_ingredient_ids
        from models import Ingredient
        missing = Ingredient.query.filter(Ingredient.id.in_(missing_ids)).all()
        
        return {
            'match_percent': match_percent,
            'missing_ingredients': [ing.to_dict() for ing in missing]
        }

