import pytest
from run import create_app
from extensions import db
from models import Consumer, Role, Ingredient, Category, Recipe

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        
        # Создаём роли
        admin_role = Role(name='admin')
        user_role = Role(name='user')
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()
        
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_user(app):
    with app.app_context():
        user_role = Role.query.filter_by(name='user').first()
        user = Consumer(
            username='testuser',
            email='test@example.com',
            password_hash='hashed_password',
            role_id=user_role.id
        )
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def test_admin(app):
    with app.app_context():
        admin_role = Role.query.filter_by(name='admin').first()
        admin = Consumer(
            username='admin',
            email='admin@example.com',
            password_hash='hashed_password',
            role_id=admin_role.id
        )
        db.session.add(admin)
        db.session.commit()
        return admin

@pytest.fixture
def test_ingredients(app):
    with app.app_context():
        ingredients = [
            Ingredient(name='курица'),
            Ingredient(name='картофель'),
            Ingredient(name='лук')
        ]
        for ing in ingredients:
            db.session.add(ing)
        db.session.commit()
        return ingredients

@pytest.fixture
def test_recipe(app, test_ingredients):
    with app.app_context():
        recipe = Recipe(
            title='Тестовый рецепт',
            description='Описание',
            cooking_time=30,
            difficulty='easy'
        )
        recipe.ingredients = test_ingredients
        db.session.add(recipe)
        db.session.commit()
        return recipe

