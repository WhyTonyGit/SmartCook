from repository import CategoryRepository

class CategoryService:
    @staticmethod
    def get_all():
        return CategoryRepository.get_all()
    
    @staticmethod
    def get_category(category_id):
        return CategoryRepository.get_by_id(category_id)

