from extensions import db
from models import Ingredient

class IngredientRepository:
    @staticmethod
    def get_by_id(ingredient_id):
        return Ingredient.query.get(ingredient_id)
    
    @staticmethod
    def get_by_name(name):
        return Ingredient.query.filter_by(name=name).first()
    
    @staticmethod
    def search(query=None, limit=100):
        q = Ingredient.query
        if query:
            q = q.filter(Ingredient.name.ilike(f'%{query}%'))
        return q.limit(limit).all()
    
    @staticmethod
    def get_by_ids(ingredient_ids):
        return Ingredient.query.filter(Ingredient.id.in_(ingredient_ids)).all()
    
    @staticmethod
    def get_by_names(names):
        return Ingredient.query.filter(Ingredient.name.in_(names)).all()
    
    @staticmethod
    def create(name, image_url=None):
        ingredient = Ingredient(name=name, image_url=image_url)
        db.session.add(ingredient)
        db.session.commit()
        return ingredient
    
    @staticmethod
    def get_all():
        return Ingredient.query.all()

