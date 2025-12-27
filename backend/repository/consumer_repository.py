from extensions import db
from models import Consumer, Role
from exception import NotFoundError

class ConsumerRepository:
    @staticmethod
    def get_by_id(consumer_id):
        return Consumer.query.get(consumer_id)
    
    @staticmethod
    def get_by_email(email):
        return Consumer.query.filter_by(email=email).first()
    
    @staticmethod
    def get_by_phone(phone):
        return Consumer.query.filter_by(phone=phone).first()
    
    @staticmethod
    def get_by_email_or_phone(email_or_phone):
        consumer = Consumer.query.filter_by(email=email_or_phone).first()
        if not consumer:
            consumer = Consumer.query.filter_by(phone=email_or_phone).first()
        return consumer
    
    @staticmethod
    def create(username, email, phone, password, role_id=2):
        consumer = Consumer(
            username=username,
            email=email,
            phone=phone,
            role_id=role_id
        )
        consumer.set_password(password)
        db.session.add(consumer)
        db.session.commit()
        return consumer
    
    @staticmethod
    def update(consumer_id, **kwargs):
        consumer = ConsumerRepository.get_by_id(consumer_id)
        if not consumer:
            raise NotFoundError("Consumer not found")
        
        for key, value in kwargs.items():
            if hasattr(consumer, key) and value is not None:
                setattr(consumer, key, value)
        
        db.session.commit()
        return consumer
    
    @staticmethod
    def set_forbidden_ingredients(consumer_id, ingredient_ids):
        consumer = ConsumerRepository.get_by_id(consumer_id)
        if not consumer:
            raise NotFoundError("Consumer not found")
        
        from models import Ingredient
        ingredients = Ingredient.query.filter(Ingredient.id.in_(ingredient_ids)).all()
        consumer.forbidden_ingredients = ingredients
        db.session.commit()
        return consumer

