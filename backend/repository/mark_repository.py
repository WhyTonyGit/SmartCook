from extensions import db
from models import Mark
from sqlalchemy import and_

class MarkRepository:
    @staticmethod
    def get_by_consumer_and_recipe(consumer_id, recipe_id):
        return Mark.query.filter(
            and_(Mark.consumer_id == consumer_id, Mark.recipe_id == recipe_id)
        ).first()
    
    @staticmethod
    def upsert(consumer_id, recipe_id, value):
        mark = MarkRepository.get_by_consumer_and_recipe(consumer_id, recipe_id)
        if mark:
            mark.value = value
        else:
            mark = Mark(consumer_id=consumer_id, recipe_id=recipe_id, value=value)
            db.session.add(mark)
        db.session.commit()
        return mark
    
    @staticmethod
    def get_by_consumer(consumer_id):
        return Mark.query.filter_by(consumer_id=consumer_id).all()
    
    @staticmethod
    def get_by_recipe(recipe_id):
        return Mark.query.filter_by(recipe_id=recipe_id).all()

