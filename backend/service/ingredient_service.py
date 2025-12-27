from repository import IngredientRepository

class IngredientService:
    @staticmethod
    def search_ingredients(query=None, limit=100):
        return IngredientRepository.search(query=query, limit=limit)
    
    @staticmethod
    def get_ingredient(ingredient_id):
        return IngredientRepository.get_by_id(ingredient_id)
    
    @staticmethod
    def get_all():
        return IngredientRepository.get_all()
    
    @staticmethod
    def resolve_ingredient_ids(ingredient_names_or_ids):
        """Преобразует список имён или ID в список ID"""
        ingredient_ids = []
        ingredient_names = []
        
        for item in ingredient_names_or_ids:
            if isinstance(item, int) or (isinstance(item, str) and item.isdigit()):
                ingredient_ids.append(int(item))
            else:
                ingredient_names.append(item.strip())
        
        # Получаем ID по именам
        if ingredient_names:
            ingredients = IngredientRepository.get_by_names(ingredient_names)
            ingredient_ids.extend([ing.id for ing in ingredients])
        
        return list(set(ingredient_ids))  # Убираем дубликаты

