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
        'курица', 'индейка', 'говядина', 'свинина', 'рыба', 'лосось', 'тунец',
        'креветки', 'кальмар', 'картофель', 'батат', 'морковь', 'лук', 'чеснок',
        'помидоры', 'черри', 'огурцы', 'перец', 'баклажаны', 'кабачки',
        'капуста', 'цветная капуста', 'брокколи', 'грибы', 'шампиньоны',
        'рис', 'гречка', 'пшено', 'овсянка', 'макароны', 'паста', 'мука',
        'яйца', 'молоко', 'сливки', 'сыр', 'творог', 'йогурт', 'масло',
        'оливковое масло', 'соль', 'сахар', 'мёд', 'лимон', 'лайм', 'яблоко',
        'банан', 'груша', 'клубника', 'черника', 'малина', 'изюм', 'орехи',
        'миндаль', 'грецкие орехи', 'кунжут', 'зелень', 'петрушка', 'укроп',
        'кинза', 'базилик', 'тимьян', 'розмарин', 'орегано', 'паприка',
        'корица', 'ваниль', 'соевый соус', 'томатная паста', 'сметана',
        'горчица', 'майонез', 'перловка', 'фасоль', 'нут', 'горох', 'кукуруза',
        'горчица зернистая', 'авокадо', 'шпинат', 'листовой салат', 'руккола',
        'болгарский перец', 'тыква', 'какао', 'шоколад'
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
    def ingredient_image_url(index):
        slot = (index % 24) + 1
        return f"/static/img/ingredients/ingredient-{slot:02d}.svg"
    
    added = 0
    skipped = 0
    
    for idx, name in enumerate(unique_ingredients):
        normalized = normalize_name(name)
        if normalized in existing_names:
            existing = existing_names[normalized]
            if not existing.image_url:
                existing.image_url = ingredient_image_url(idx)
            skipped += 1
        else:
            ingredient = Ingredient(
                name=name.strip(),
                image_url=ingredient_image_url(idx)
            )
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
        'Супы', 'Выпечка', 'Напитки', 'Закуски', 'Вегетарианские',
        'Мясо', 'Паста', 'Все блюда'
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
    
    ingredients_pool = Ingredient.query.all()
    categories_pool = {normalize_name(cat.name): cat for cat in Category.query.all()}

    def recipe_image_url(index):
        slot = (index % 24) + 1
        return f"/static/img/recipes/recipe-{slot:02d}.svg"

    def pick_categories(title):
        key = normalize_name(title)
        picked = []
        def add(name):
            cat = categories_pool.get(normalize_name(name))
            if cat and cat not in picked:
                picked.append(cat)

        if 'суп' in key:
            add('Супы')
        if 'салат' in key:
            add('Салаты')
        if 'паста' in key:
            add('Паста')
        if 'десерт' in key or 'сырник' in key or 'блины' in key:
            add('Десерты')
        if 'смус' in key or 'напит' in key:
            add('Напитки')
        if 'омлет' in key or 'каша' in key:
            add('Завтраки')
        if any(word in key for word in ['куриц', 'говядин', 'свин', 'котлет', 'гуляш', 'филе']):
            add('Мясо')
        if not picked:
            add('Все блюда')
        add('Обеды')
        return picked

    adjectives = ['Домашний', 'Нежный', 'Пряный', 'Сливочный', 'Лёгкий', 'Сытный', 'Запечённый', 'Тёплый', 'Хрустящий', 'Ароматный']
    bases = [
        'суп', 'салат', 'рагу', 'боул', 'плов', 'омлет', 'паста', 'запеканка',
        'гуляш', 'тушёные овощи', 'рис', 'картофель', 'куриное филе', 'котлеты',
        'десерт', 'блины', 'сырники', 'смузи', 'каша', 'бутерброд', 'овощное ассорти',
        'рыбный стейк', 'гратен', 'овощной соте', 'тёплый салат'
    ]

    titles = []
    for adj in adjectives:
        for base in bases:
            titles.append(f"{adj} {base}")
    titles = titles[:70]

    import hashlib
    import random

    recipes_to_create = []
    updated_existing = 0
    for idx, title in enumerate(titles):
        normalized_title = normalize_name(title)
        if normalized_title in existing_recipes:
            existing = existing_recipes[normalized_title]
            if not existing.image_url:
                existing.image_url = recipe_image_url(idx)
                updated_existing += 1
            continue

        seed = int(hashlib.md5(normalized_title.encode('utf-8')).hexdigest(), 16)
        rng = random.Random(seed)
        count = 5 + (seed % 8)
        picked_ingredients = rng.sample(ingredients_pool, min(count, len(ingredients_pool)))

        recipe = Recipe(
            title=title,
            description=f"{title.capitalize()} с акцентом на свежие продукты.",
            cooking_time=20 + (seed % 50),
            difficulty=[Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD][seed % 3],
            image_url=recipe_image_url(idx)
        )
        recipe.ingredients = picked_ingredients
        recipe.categories = pick_categories(title)

        learning = Learning(title=f"Как приготовить {title.lower()}", recipe=recipe)
        learning.steps = [
            StepLearning(title='Подготовка', description='Подготовьте ингредиенты и посуду.', number=1, learning=learning),
            StepLearning(title='Готовка', description='Готовьте на среднем огне до готовности.', number=2, learning=learning),
            StepLearning(title='Подача', description='Подавайте блюдо тёплым.', number=3, learning=learning)
        ]
        recipe.learning = learning
        recipes_to_create.append(recipe)
    
    if recipes_to_create:
        for recipe in recipes_to_create:
            db.session.add(recipe)
        db.session.commit()
        print(f"✓ Recipes: {len(recipes_to_create)} added, {len(existing_recipes)} already exist")
    else:
        if updated_existing:
            db.session.commit()
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
