from extensions import db
from models import Category

class CategoryRepository:
    @staticmethod
    def get_by_id(category_id):
        return Category.query.get(category_id)
    
    @staticmethod
    def get_by_name(name):
        return Category.query.filter_by(name=name).first()
    
    @staticmethod
    def get_all():
        return Category.query.all()
    
    @staticmethod
    def create(name):
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category

