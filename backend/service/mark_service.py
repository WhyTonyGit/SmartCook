from repository import MarkRepository
from exception import ValidationError

class MarkService:
    @staticmethod
    def upsert_mark(recipe_id, consumer_id, value):
        if not (1 <= value <= 5):
            raise ValidationError("Mark value must be between 1 and 5")
        return MarkRepository.upsert(consumer_id, recipe_id, value)
    
    @staticmethod
    def get_marks(consumer_id):
        return MarkRepository.get_by_consumer(consumer_id)

    @staticmethod
    def delete_mark(recipe_id, consumer_id):
        return MarkRepository.delete_by_consumer_and_recipe(consumer_id, recipe_id)
