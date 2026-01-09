import re
from extensions import db
from models import Ingredient

class IngredientRepository:
    @staticmethod
    def _normalize_name(name):
        if not name:
            return ''
        normalized = name.strip().lower().replace('ё', 'е')
        return re.sub(r'\s+', ' ', normalized)

    @staticmethod
    def get_by_id(ingredient_id):
        return Ingredient.query.get(ingredient_id)
    
    @staticmethod
    def get_by_name(name):
        return Ingredient.query.filter_by(name=name).first()
    
    @staticmethod
    def search(query=None, limit=100):
        q = Ingredient.query
        if not query:
            return q.limit(limit).all()

        normalized_query = IngredientRepository._normalize_name(query)
        if not normalized_query:
            return []

        ingredients = q.all()
        matched = []
        for ing in ingredients:
            ing_name = IngredientRepository._normalize_name(ing.name)
            if normalized_query in ing_name:
                matched.append(ing)
                if len(matched) >= limit:
                    break
        return matched
    
    @staticmethod
    def get_by_ids(ingredient_ids):
        return Ingredient.query.filter(Ingredient.id.in_(ingredient_ids)).all()
    
    @staticmethod
    def get_by_names(names):
        normalized_names = [
            IngredientRepository._normalize_name(name)
            for name in names
            if IngredientRepository._normalize_name(name)
        ]
        if not normalized_names:
            return []
        ingredients = Ingredient.query.all()
        matched = []
        for ing in ingredients:
            ing_name = IngredientRepository._normalize_name(ing.name)
            if any(query in ing_name or ing_name in query for query in normalized_names):
                matched.append(ing)
        return matched
    
    @staticmethod
    def create(name, image_url=None):
        ingredient = Ingredient(name=name, image_url=image_url)
        db.session.add(ingredient)
        db.session.commit()
        return ingredient
    
    @staticmethod
    def get_all():
        return Ingredient.query.all()
