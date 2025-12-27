"""
Seed script для загрузки начальных данных
Использование: python seed.py
"""
import csv
import os
from run import create_app
from extensions import db
from models import Consumer, Role, Ingredient, Category, Recipe, Learning, StepLearning
from models.recipe import Difficulty
from werkzeug.security import generate_password_hash

def seed_roles():
    """Создаёт роли"""
    if Role.query.count() == 0:
        admin_role = Role(name='admin')
        user_role = Role(name='user')
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()
        print("✓ Roles seeded")
    else:
        print("✓ Roles already exist")

def seed_admin():
    """Создаёт администратора"""
    admin = Consumer.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin_role = Role.query.filter_by(name='admin').first()
        admin = Consumer(
            username='admin',
            email='admin@example.com',
            phone=None,
            password_hash=generate_password_hash('Admin123!'),
            role_id=admin_role.id
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Admin user created")
    else:
        print("✓ Admin user already exists")

def seed_ingredients():
    """Загружает ингредиенты из CSV или создаёт базовые"""
    if Ingredient.query.count() > 0:
        print("✓ Ingredients already exist")
        return
    
    ingredients_data = [
        'курица', 'картофель', 'морковь', 'лук', 'чеснок', 'помидоры',
        'огурцы', 'перец', 'баклажаны', 'кабачки', 'капуста', 'рис',
        'макароны', 'мука', 'яйца', 'молоко', 'сливки', 'сыр',
        'масло', 'соль', 'перец', 'сахар', 'мускатный орех', 'базилик',
        'петрушка', 'укроп', 'тимьян', 'розмарин', 'орегано', 'паприка'
    ]
    
    for name in ingredients_data:
        ingredient = Ingredient(name=name)
        db.session.add(ingredient)
    
    db.session.commit()
    print(f"✓ {len(ingredients_data)} ingredients seeded")

def seed_categories():
    """Загружает категории"""
    if Category.query.count() > 0:
        print("✓ Categories already exist")
        return
    
    categories_data = [
        'Завтраки', 'Обеды', 'Ужины', 'Десерты', 'Салаты',
        'Супы', 'Выпечка', 'Напитки', 'Закуски', 'Вегетарианские'
    ]
    
    for name in categories_data:
        category = Category(name=name)
        db.session.add(category)
    
    db.session.commit()
    print(f"✓ {len(categories_data)} categories seeded")

def seed_recipes():
    """Создаёт демо-рецепты"""
    if Recipe.query.count() > 0:
        print("✓ Recipes already exist")
        return
    
    # Получаем ингредиенты и категории
    chicken = Ingredient.query.filter_by(name='курица').first()
    potato = Ingredient.query.filter_by(name='картофель').first()
    carrot = Ingredient.query.filter_by(name='морковь').first()
    onion = Ingredient.query.filter_by(name='лук').first()
    garlic = Ingredient.query.filter_by(name='чеснок').first()
    salt = Ingredient.query.filter_by(name='соль').first()
    pepper = Ingredient.query.filter_by(name='перец').first()
    oil = Ingredient.query.filter_by(name='масло').first()
    
    lunch_cat = Category.query.filter_by(name='Обеды').first()
    dinner_cat = Category.query.filter_by(name='Ужины').first()
    
    # Рецепт 1: Жареная курица с картофелем
    recipe1 = Recipe(
        title='Жареная курица с картофелем',
        description='Простое и сытное блюдо из курицы и картофеля',
        cooking_time=45,
        difficulty=Difficulty.EASY
    )
    recipe1.ingredients = [chicken, potato, onion, garlic, salt, pepper, oil]
    recipe1.categories = [lunch_cat, dinner_cat]
    
    learning1 = Learning(title='Как приготовить жареную курицу с картофелем', recipe=recipe1)
    step1 = StepLearning(
        title='Подготовка ингредиентов',
        description='Нарежьте курицу на кусочки, картофель на дольки, лук полукольцами',
        number=1,
        learning=learning1
    )
    step2 = StepLearning(
        title='Обжарка',
        description='Обжарьте курицу на масле до золотистой корочки, добавьте картофель и лук',
        number=2,
        learning=learning1
    )
    step3 = StepLearning(
        title='Готовка',
        description='Тушите под крышкой 30 минут на среднем огне',
        number=3,
        learning=learning1
    )
    learning1.steps = [step1, step2, step3]
    recipe1.learning = learning1
    
    db.session.add(recipe1)
    
    # Рецепт 2: Картофельное пюре
    recipe2 = Recipe(
        title='Картофельное пюре',
        description='Классическое картофельное пюре',
        cooking_time=25,
        difficulty=Difficulty.EASY
    )
    recipe2.ingredients = [potato, salt, oil]
    recipe2.categories = [lunch_cat]
    
    learning2 = Learning(title='Как приготовить картофельное пюре', recipe=recipe2)
    step1 = StepLearning(
        title='Варка картофеля',
        description='Отварите картофель в подсоленной воде до готовности',
        number=1,
        learning=learning2
    )
    step2 = StepLearning(
        title='Приготовление пюре',
        description='Разомните картофель, добавьте масло и соль по вкусу',
        number=2,
        learning=learning2
    )
    learning2.steps = [step1, step2]
    recipe2.learning = learning2
    
    db.session.add(recipe2)
    
    # Рецепт 3: Куриный суп
    recipe3 = Recipe(
        title='Куриный суп',
        description='Наваристый куриный суп с овощами',
        cooking_time=60,
        difficulty=Difficulty.MEDIUM
    )
    recipe3.ingredients = [chicken, carrot, onion, potato, salt, pepper]
    recipe3.categories = [lunch_cat]
    
    learning3 = Learning(title='Как приготовить куриный суп', recipe=recipe3)
    step1 = StepLearning(
        title='Бульон',
        description='Сварите курицу в подсоленной воде 40 минут',
        number=1,
        learning=learning3
    )
    step2 = StepLearning(
        title='Овощи',
        description='Добавьте нарезанные овощи и варите ещё 20 минут',
        number=2,
        learning=learning3
    )
    learning3.steps = [step1, step2]
    recipe3.learning = learning3
    
    db.session.add(recipe3)
    
    db.session.commit()
    print("✓ 3 demo recipes seeded")

def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_roles()
        seed_admin()
        seed_ingredients()
        seed_categories()
        seed_recipes()
        print("\n✓ Seeding completed!")

if __name__ == '__main__':
    main()

