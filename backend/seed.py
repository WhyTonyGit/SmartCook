"""
Seed script для загрузки начальных данных
Использование: 
  python seed.py          # Добавить недостающие данные
  python seed.py --reset  # Очистить и загрузить заново
"""
import sys
import re
from run import create_app
from extensions import db
from models import Consumer, Role, Ingredient, Category, Recipe, Difficulty, Learning, StepLearning
from werkzeug.security import generate_password_hash

def normalize_name(name):
    """Нормализует имя: strip, lower, множественные пробелы -> один"""
    if not name:
        return ''
    normalized = re.sub(r'\s+', ' ', name.strip().lower())
    return normalized

def seed_roles(reset=False):
    """Создаёт роли"""
    if reset:
        Role.query.delete()
        db.session.commit()
        print("✓ Roles cleared")
    
    roles_data = ['admin', 'user']
    added = 0
    skipped = 0
    
    for role_name in roles_data:
        normalized = normalize_name(role_name)
        existing = Role.query.filter_by(name=normalized).first()
        if not existing:
            role = Role(name=normalized)
            db.session.add(role)
            added += 1
        else:
            skipped += 1
    
    db.session.commit()
    print(f"✓ Roles: {added} added, {skipped} skipped")

def seed_admin(reset=False):
    """Создаёт администратора"""
    if reset:
        Consumer.query.filter_by(email='admin@example.com').delete()
        db.session.commit()
        print("✓ Admin user cleared")
    
    admin = Consumer.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            print("⚠ Admin role not found, creating...")
            admin_role = Role(name='admin')
            db.session.add(admin_role)
            db.session.commit()
        
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

def seed_ingredients(reset=False):
    """Загружает ингредиенты с дедупликацией и upsert"""
    if reset:
        Ingredient.query.delete()
        db.session.commit()
        print("✓ Ingredients cleared")
    
    ingredients_data = [
        'курица', 'картофель', 'морковь', 'лук', 'чеснок', 'помидоры',
        'огурцы', 'перец', 'баклажаны', 'кабачки', 'капуста', 'рис',
        'макароны', 'мука', 'яйца', 'молоко', 'сливки', 'сыр',
        'масло', 'соль', 'сахар', 'мускатный орех', 'базилик',
        'петрушка', 'укроп', 'тимьян', 'розмарин', 'орегано', 'паприка'
    ]
    
    # Дедупликация по нормализованному имени
    seen = set()
    unique_ingredients = []
    for name in ingredients_data:
        normalized = normalize_name(name)
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique_ingredients.append(name)  # Сохраняем оригинальное имя для вставки
    
    # Получаем существующие ингредиенты
    existing_names = {normalize_name(ing.name): ing for ing in Ingredient.query.all()}
    
    added = 0
    skipped = 0
    
    for name in unique_ingredients:
        normalized = normalize_name(name)
        if normalized in existing_names:
            skipped += 1
        else:
            ingredient = Ingredient(name=name.strip())  # Сохраняем оригинальное имя
            db.session.add(ingredient)
            added += 1
    
    db.session.commit()
    print(f"✓ Ingredients: {added} added, {skipped} skipped (total unique: {len(unique_ingredients)})")

def seed_categories(reset=False):
    """Загружает категории с дедупликацией и upsert"""
    if reset:
        Category.query.delete()
        db.session.commit()
        print("✓ Categories cleared")
    
    categories_data = [
        'Завтраки', 'Обеды', 'Ужины', 'Десерты', 'Салаты',
        'Супы', 'Выпечка', 'Напитки', 'Закуски', 'Вегетарианские'
    ]
    
    # Дедупликация
    seen = set()
    unique_categories = []
    for name in categories_data:
        normalized = normalize_name(name)
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique_categories.append(name)
    
    # Получаем существующие категории
    existing_names = {normalize_name(cat.name): cat for cat in Category.query.all()}
    
    added = 0
    skipped = 0
    
    for name in unique_categories:
        normalized = normalize_name(name)
        if normalized in existing_names:
            skipped += 1
        else:
            category = Category(name=name.strip())
            db.session.add(category)
            added += 1
    
    db.session.commit()
    print(f"✓ Categories: {added} added, {skipped} skipped (total unique: {len(unique_categories)})")

def seed_recipes(reset=False):
    """Создаёт демо-рецепты с проверкой на существование"""
    if reset:
        # Удаляем в правильном порядке (сначала зависимые)
        StepLearning.query.delete()
        Learning.query.delete()
        Recipe.query.delete()
        db.session.commit()
        print("✓ Recipes cleared")
    
    # Проверяем, есть ли уже рецепты
    existing_recipes = {r.title.lower(): r for r in Recipe.query.all()}
    
    # Получаем ингредиенты и категории
    def get_ingredient(name):
        # Пробуем найти по точному совпадению
        ing = Ingredient.query.filter_by(name=name).first()
        if not ing:
            # Пробуем найти по нормализованному имени
            normalized = normalize_name(name)
            for existing_ing in Ingredient.query.all():
                if normalize_name(existing_ing.name) == normalized:
                    return existing_ing
        return ing
    
    def get_category(name):
        cat = Category.query.filter_by(name=name).first()
        if not cat:
            normalized = normalize_name(name)
            for existing_cat in Category.query.all():
                if normalize_name(existing_cat.name) == normalized:
                    return existing_cat
        return cat
    
    chicken = get_ingredient('курица')
    potato = get_ingredient('картофель')
    carrot = get_ingredient('морковь')
    onion = get_ingredient('лук')
    garlic = get_ingredient('чеснок')
    salt = get_ingredient('соль')
    pepper = get_ingredient('перец')
    oil = get_ingredient('масло')
    
    lunch_cat = get_category('Обеды')
    dinner_cat = get_category('Ужины')
    
    recipes_to_create = []
    
    # Рецепт 1: Жареная курица с картофелем
    recipe1_title = 'Жареная курица с картофелем'
    if normalize_name(recipe1_title) not in existing_recipes:
        recipe1 = Recipe(
            title=recipe1_title,
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
        recipes_to_create.append(recipe1)
    
    # Рецепт 2: Картофельное пюре
    recipe2_title = 'Картофельное пюре'
    if normalize_name(recipe2_title) not in existing_recipes:
        recipe2 = Recipe(
            title=recipe2_title,
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
        recipes_to_create.append(recipe2)
    
    # Рецепт 3: Куриный суп
    recipe3_title = 'Куриный суп'
    if normalize_name(recipe3_title) not in existing_recipes:
        recipe3 = Recipe(
            title=recipe3_title,
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
        recipes_to_create.append(recipe3)
    
    if recipes_to_create:
        for recipe in recipes_to_create:
            db.session.add(recipe)
        db.session.commit()
        print(f"✓ Recipes: {len(recipes_to_create)} added, {len(existing_recipes)} already exist")
    else:
        print(f"✓ Recipes: 0 added, {len(existing_recipes)} already exist")

def main():
    reset = '--reset' in sys.argv
    
    app = create_app()
    with app.app_context():
        db.create_all()
        
        if reset:
            print("⚠ Reset mode: clearing existing data...")
        
        seed_roles(reset=reset)
        seed_admin(reset=reset)
        seed_ingredients(reset=reset)
        seed_categories(reset=reset)
        seed_recipes(reset=reset)
        
        print("\n✓ Seeding completed!")

if __name__ == '__main__':
    main()
