"""
Seed script для загрузки начальных данных
Использование: 
  python seed.py          # Добавить недостающие данные
  python seed.py --reset  # Очистить и загрузить заново
"""
import sys
import re
from urllib.parse import quote_plus
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
        'курица', 'индейка', 'говядина', 'свинина', 'баранина', 'кролик', 'рыба',
        'лосось', 'тунец', 'треска', 'креветки', 'кальмар', 'мидии', 'бекон',
        'картофель', 'батат', 'морковь', 'лук', 'чеснок', 'помидоры', 'черри',
        'огурцы', 'перец', 'болгарский перец', 'баклажаны', 'кабачки', 'цукини',
        'капуста', 'цветная капуста', 'брокколи', 'шпинат', 'листовой салат',
        'руккола', 'свекла', 'тыква', 'кукуруза', 'зелёный горошек', 'оливки',
        'грибы', 'шампиньоны', 'сельдерей', 'авокадо',
        'рис', 'басмати', 'гречка', 'пшено', 'овсянка', 'перловка', 'булгур',
        'кускус', 'макароны', 'паста', 'лапша', 'мука', 'крахмал',
        'фасоль', 'нут', 'чечевица', 'горох',
        'яйца', 'молоко', 'кефир', 'сливки', 'сыр', 'творог', 'йогурт',
        'сметана', 'сливочное масло', 'оливковое масло', 'растительное масло',
        'соль', 'сахар', 'сахарная пудра', 'мёд', 'лимон', 'лайм', 'уксус',
        'соевый соус', 'томатная паста', 'горчица', 'майонез', 'аджика',
        'яблоко', 'банан', 'груша', 'клубника', 'черника', 'малина', 'изюм',
        'курага', 'финики',
        'орехи', 'миндаль', 'грецкие орехи', 'кунжут', 'семена подсолнуха',
        'семена тыквы', 'семена чиа',
        'зелень', 'петрушка', 'укроп', 'кинза', 'базилик', 'тимьян', 'розмарин',
        'орегано', 'паприка', 'корица', 'ваниль', 'мускатный орех',
        'какао', 'шоколад', 'разрыхлитель', 'дрожжи', 'сухари'
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
        {'name': 'Завтраки', 'query': 'breakfast'},
        {'name': 'Обеды', 'query': 'pasta'},
        {'name': 'Ужины', 'query': 'meat'},
        {'name': 'Десерты', 'query': 'dessert'},
        {'name': 'Салаты', 'query': 'salad'},
        {'name': 'Супы', 'query': 'soup'},
        {'name': 'Выпечка', 'query': 'baking'},
        {'name': 'Напитки', 'query': 'drink'},
        {'name': 'Закуски', 'query': 'appetizer'},
        {'name': 'Вегетарианские', 'query': 'vegetarian'},
        {'name': 'Мясо', 'query': 'meat'},
        {'name': 'Паста', 'query': 'pasta'},
        {'name': 'Все блюда', 'query': 'appetizer'}
    ]
    
    # Дедупликация
    seen = set()
    unique_categories = []
    for item in categories_data:
        name = item['name']
        normalized = normalize_name(name)
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique_categories.append(item)
    
    # Получаем существующие категории
    existing_names = {normalize_name(cat.name): cat for cat in Category.query.all()}
    
    added = 0
    skipped = 0
    
    def category_image_url(query):
        return f"https://source.unsplash.com/960x640/?{query}"

    for item in unique_categories:
        name = item['name']
        normalized = normalize_name(name)
        image_url = category_image_url(item['query'])
        if normalized in existing_names:
            existing = existing_names[normalized]
            existing.image_url = image_url
            skipped += 1
        else:
            category = Category(name=name.strip(), image_url=image_url)
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

    def recipe_image_url(query):
        return f"https://source.unsplash.com/960x640/?{quote_plus(query)}"

    recipes_data = [
        {
            'title': 'Омлет с овощами',
            'description': 'Пышный омлет с обжаренными овощами и ароматной зеленью.',
            'cooking_time': 18,
            'difficulty': Difficulty.EASY,
            'image_query': 'omelet',
            'categories': ['Завтраки'],
            'ingredients': ['яйца', 'молоко', 'болгарский перец', 'помидоры', 'лук', 'зелень', 'соль'],
            'steps': [
                ('Подготовка овощей', 'Нарежьте перец и помидоры кубиком, лук — тонкими полукольцами.'),
                ('Обжарка основы', 'Разогрейте сковороду с небольшим количеством масла и обжарьте лук 2–3 минуты.'),
                ('Добавление овощей', 'Добавьте перец и помидоры, готовьте ещё 3–4 минуты до мягкости.'),
                ('Яичная смесь', 'Взбейте яйца с молоком, посолите и добавьте щепотку перца.'),
                ('Готовка', 'Влейте смесь к овощам, накройте крышкой и готовьте 4–5 минут на слабом огне.'),
                ('Подача', 'Снимите омлет с огня и посыпьте свежей зеленью перед подачей.')
            ]
        },
        {
            'title': 'Овсяная каша с ягодами',
            'description': 'Нежная овсяная каша на молоке с мёдом и свежими ягодами.',
            'cooking_time': 15,
            'difficulty': Difficulty.EASY,
            'image_query': 'oatmeal berries',
            'categories': ['Завтраки'],
            'ingredients': ['овсянка', 'молоко', 'мёд', 'клубника', 'черника', 'сливочное масло'],
            'steps': [
                ('Подготовка крупы', 'Промойте овсянку, чтобы удалить лишнюю пыль.'),
                ('Нагрев молока', 'Доведите молоко до лёгкого кипения в кастрюле.'),
                ('Варка каши', 'Всыпьте овсянку и варите 5–7 минут на слабом огне, помешивая.'),
                ('Добавление вкуса', 'Добавьте кусочек сливочного масла и перемешайте.'),
                ('Сладость', 'Снимите с огня и вмешайте мёд.'),
                ('Подача', 'Разложите кашу по тарелкам и добавьте свежие ягоды сверху.')
            ]
        },
        {
            'title': 'Тыквенный крем-суп',
            'description': 'Согревающий крем-суп из тыквы со сливками и пряностями.',
            'cooking_time': 35,
            'difficulty': Difficulty.EASY,
            'image_query': 'pumpkin soup',
            'categories': ['Супы'],
            'ingredients': ['тыква', 'лук', 'чеснок', 'сливки', 'оливковое масло', 'тимьян', 'соль'],
            'steps': [
                ('Подготовка овощей', 'Нарежьте тыкву кубиком, лук — полукольцами, чеснок — пластинами.'),
                ('Обжарка', 'Разогрейте масло, обжарьте лук и чеснок до мягкости 3–4 минуты.'),
                ('Добавление тыквы', 'Выложите тыкву, перемешайте и готовьте ещё 4–5 минут.'),
                ('Варка', 'Залейте горячей водой так, чтобы покрыть овощи, и варите 15–18 минут.'),
                ('Пюрирование', 'Пробейте суп блендером до гладкой текстуры.'),
                ('Финальный штрих', 'Влейте сливки, посолите, добавьте тимьян и прогрейте 2 минуты.')
            ]
        },
        {
            'title': 'Курица терияки с рисом',
            'description': 'Сочная курица в соусе терияки с рассыпчатым рисом и кунжутом.',
            'cooking_time': 30,
            'difficulty': Difficulty.MEDIUM,
            'image_query': 'teriyaki chicken',
            'categories': ['Обеды', 'Ужины', 'Мясо'],
            'ingredients': ['курица', 'рис', 'соевый соус', 'мёд', 'чеснок', 'кунжут', 'оливковое масло'],
            'steps': [
                ('Подготовка риса', 'Промойте рис и сварите до готовности в подсоленной воде.'),
                ('Маринад', 'Смешайте соевый соус, мёд и измельчённый чеснок.'),
                ('Маринование', 'Нарежьте курицу ломтиками и замаринуйте в соусе на 10 минут.'),
                ('Обжарка', 'Обжарьте курицу на разогретой сковороде 4–5 минут до румяности.'),
                ('Уваривание соуса', 'Влейте остатки маринада и готовьте ещё 2–3 минуты до загустения.'),
                ('Подача', 'Разложите рис, сверху курицу, посыпьте кунжутом.')
            ]
        },
        {
            'title': 'Паста карбонара',
            'description': 'Классическая паста в сливочно-яичном соусе с беконом и сыром.',
            'cooking_time': 25,
            'difficulty': Difficulty.MEDIUM,
            'image_query': 'carbonara pasta',
            'categories': ['Паста'],
            'ingredients': ['паста', 'бекон', 'яйца', 'сыр', 'сливки', 'чеснок', 'соль'],
            'steps': [
                ('Варка пасты', 'Отварите пасту до состояния al dente в подсоленной воде.'),
                ('Обжарка бекона', 'Нарежьте бекон и обжарьте до хруста, добавьте чеснок на 30 секунд.'),
                ('Соус', 'Смешайте яйца, сливки и тёртый сыр до однородности.'),
                ('Соединение', 'Слейте воду с пасты, добавьте к бекону и перемешайте.'),
                ('Смешивание', 'Снимите с огня и быстро вмешайте яичный соус, чтобы он стал кремовым.'),
                ('Подача', 'Добавьте щепотку соли и подавайте сразу.')
            ]
        },
        {
            'title': 'Салат Цезарь',
            'description': 'Хрустящий салат с курицей, сухариками и пикантным соусом.',
            'cooking_time': 20,
            'difficulty': Difficulty.EASY,
            'image_query': 'caesar salad',
            'categories': ['Салаты'],
            'ingredients': ['курица', 'листовой салат', 'сыр', 'сухари', 'майонез', 'лимон', 'чеснок', 'горчица', 'черри'],
            'steps': [
                ('Подготовка курицы', 'Нарежьте курицу полосками и обжарьте до золотистой корочки.'),
                ('Соус', 'Смешайте майонез, лимонный сок, чеснок и горчицу до однородности.'),
                ('Салатная база', 'Порвите листья салата руками и переложите в миску.'),
                ('Сборка', 'Добавьте курицу и сухари, перемешайте.'),
                ('Заправка', 'Полейте соусом и аккуратно перемешайте.'),
                ('Финал', 'Посыпьте тёртым сыром и добавьте половинки черри.')
            ]
        },
        {
            'title': 'Греческий салат',
            'description': 'Свежий салат с овощами, сыром и оливковым маслом.',
            'cooking_time': 15,
            'difficulty': Difficulty.EASY,
            'image_query': 'greek salad',
            'categories': ['Салаты'],
            'ingredients': ['огурцы', 'помидоры', 'болгарский перец', 'оливки', 'сыр', 'оливковое масло', 'орегано', 'соль'],
            'steps': [
                ('Подготовка овощей', 'Нарежьте огурцы, помидоры и перец крупными кубиками.'),
                ('Добавление оливок', 'Разрежьте оливки пополам и добавьте к овощам.'),
                ('Сыр', 'Нарежьте сыр кубиками и аккуратно смешайте.'),
                ('Заправка', 'Полейте оливковым маслом и посолите по вкусу.'),
                ('Аромат', 'Посыпьте орегано и слегка перемешайте.'),
                ('Подача', 'Дайте салату настояться 5 минут перед подачей.')
            ]
        },
        {
            'title': 'Борщ домашний',
            'description': 'Насыщенный борщ с овощами и говядиной.',
            'cooking_time': 75,
            'difficulty': Difficulty.MEDIUM,
            'image_query': 'borscht',
            'categories': ['Супы'],
            'ingredients': ['говядина', 'свекла', 'капуста', 'картофель', 'морковь', 'лук', 'томатная паста', 'чеснок', 'соль'],
            'steps': [
                ('Бульон', 'Отварите говядину в воде 40–50 минут до мягкости.'),
                ('Подготовка овощей', 'Нарежьте свеклу и морковь соломкой, лук — кубиком.'),
                ('Пассеровка', 'Обжарьте лук с морковью, добавьте свеклу и томатную пасту, тушите 7 минут.'),
                ('Добавление картофеля', 'В бульон добавьте нарезанный картофель и варите 10 минут.'),
                ('Капуста', 'Положите нашинкованную капусту и варите ещё 7–8 минут.'),
                ('Сборка', 'Добавьте овощную заправку и чеснок, посолите.'),
                ('Настой', 'Дайте борщу настояться под крышкой 10 минут.')
            ]
        },
        {
            'title': 'Рагу из овощей',
            'description': 'Лёгкое овощное рагу с томатами и ароматными травами.',
            'cooking_time': 30,
            'difficulty': Difficulty.EASY,
            'image_query': 'vegetable stew',
            'categories': ['Вегетарианские'],
            'ingredients': ['баклажаны', 'кабачки', 'помидоры', 'морковь', 'лук', 'чеснок', 'оливковое масло', 'базилик'],
            'steps': [
                ('Подготовка', 'Нарежьте баклажаны и кабачки кубиком, морковь — полукружьями.'),
                ('Обжарка лука', 'Обжарьте лук с чесноком 2 минуты до аромата.'),
                ('Добавление овощей', 'Выложите морковь, затем баклажаны и кабачки, готовьте 5 минут.'),
                ('Томаты', 'Добавьте нарезанные помидоры и тушите 10 минут под крышкой.'),
                ('Приправы', 'Посолите и добавьте свежий базилик.'),
                ('Подача', 'Дайте рагу настояться 5 минут перед подачей.')
            ]
        },
        {
            'title': 'Запечённый лосось с лимоном',
            'description': 'Нежный лосось, запечённый с лимоном и травами.',
            'cooking_time': 25,
            'difficulty': Difficulty.EASY,
            'image_query': 'baked salmon',
            'categories': ['Ужины'],
            'ingredients': ['лосось', 'лимон', 'оливковое масло', 'тимьян', 'соль'],
            'steps': [
                ('Подготовка', 'Разогрейте духовку до 200°C.'),
                ('Маринад', 'Смешайте масло, лимонный сок и тимьян.'),
                ('Рыба', 'Натрите лосось солью и смажьте маринадом.'),
                ('Запекание', 'Выложите рыбу на противень и запекайте 12–15 минут.'),
                ('Отдых', 'Дайте рыбе отдохнуть 2 минуты после духовки.'),
                ('Подача', 'Подавайте с дольками лимона и зеленью.')
            ]
        },
        {
            'title': 'Картофельное пюре с грибами',
            'description': 'Нежное пюре с обжаренными грибами и сливочным вкусом.',
            'cooking_time': 35,
            'difficulty': Difficulty.EASY,
            'image_query': 'mashed potatoes mushrooms',
            'categories': ['Обеды'],
            'ingredients': ['картофель', 'молоко', 'сливочное масло', 'грибы', 'лук', 'соль'],
            'steps': [
                ('Отваривание картофеля', 'Очистите картофель, нарежьте и сварите до мягкости.'),
                ('Обжарка грибов', 'Нарежьте грибы и лук, обжарьте на масле до золотистости.'),
                ('Пюре', 'Слейте воду с картофеля и разомните.'),
                ('Добавление молока', 'Влейте тёплое молоко и добавьте сливочное масло.'),
                ('Смешивание', 'Перемешайте до кремовой текстуры, посолите.'),
                ('Подача', 'Выложите пюре, сверху добавьте обжаренные грибы.')
            ]
        },
        {
            'title': 'Котлеты из индейки',
            'description': 'Сочные котлеты из индейки с мягкой текстурой.',
            'cooking_time': 30,
            'difficulty': Difficulty.MEDIUM,
            'image_query': 'turkey patties',
            'categories': ['Мясо'],
            'ingredients': ['индейка', 'лук', 'яйца', 'сухари', 'чеснок', 'соль'],
            'steps': [
                ('Подготовка фарша', 'Измельчите индейку или используйте готовый фарш.'),
                ('Добавки', 'Добавьте мелко нарезанный лук, чеснок и яйцо.'),
                ('Связка', 'Всыпьте сухари и тщательно перемешайте массу.'),
                ('Формование', 'Сформируйте котлеты одинакового размера.'),
                ('Обжарка', 'Обжарьте котлеты по 4–5 минут с каждой стороны.'),
                ('Доведение', 'Накройте крышкой и готовьте ещё 3–4 минуты.'),
                ('Подача', 'Подавайте с овощным гарниром или салатом.')
            ]
        },
        {
            'title': 'Тёплый салат с креветками',
            'description': 'Салат с сочными креветками и пряной заправкой.',
            'cooking_time': 20,
            'difficulty': Difficulty.MEDIUM,
            'image_query': 'shrimp salad',
            'categories': ['Салаты'],
            'ingredients': ['креветки', 'руккола', 'черри', 'чеснок', 'оливковое масло', 'лимон', 'соль'],
            'steps': [
                ('Подготовка креветок', 'Очистите креветки и обсушите.'),
                ('Обжарка', 'Обжарьте чеснок в масле 1 минуту, добавьте креветки и готовьте 3–4 минуты.'),
                ('Листья салата', 'Разложите рукколу по тарелкам.'),
                ('Добавление овощей', 'Разрежьте черри пополам и добавьте к салату.'),
                ('Заправка', 'Смешайте лимонный сок, масло и соль, полейте салат.'),
                ('Подача', 'Выложите тёплые креветки сверху и подавайте сразу.')
            ]
        },
        {
            'title': 'Овощная паста с томатами',
            'description': 'Паста с томатами и свежими травами.',
            'cooking_time': 25,
            'difficulty': Difficulty.EASY,
            'image_query': 'pasta tomato',
            'categories': ['Паста', 'Вегетарианские'],
            'ingredients': ['паста', 'помидоры', 'чеснок', 'оливковое масло', 'базилик', 'соль'],
            'steps': [
                ('Паста', 'Отварите пасту до al dente в подсоленной воде.'),
                ('Соус', 'Обжарьте чеснок на масле 1 минуту, добавьте нарезанные помидоры.'),
                ('Тушение', 'Готовьте томаты 5–6 минут до мягкости.'),
                ('Соединение', 'Добавьте пасту в сковороду и перемешайте.'),
                ('Аромат', 'Вмешайте листья базилика и щепотку соли.'),
                ('Подача', 'Подавайте горячей с дополнительными травами.')
            ]
        },
        {
            'title': 'Фриттата со шпинатом',
            'description': 'Итальянский омлет со шпинатом и сыром.',
            'cooking_time': 22,
            'difficulty': Difficulty.EASY,
            'image_query': 'frittata spinach',
            'categories': ['Завтраки'],
            'ingredients': ['яйца', 'шпинат', 'сыр', 'молоко', 'лук', 'соль'],
            'steps': [
                ('Подготовка', 'Разогрейте духовку до 190°C.'),
                ('Обжарка лука', 'Обжарьте лук 2 минуты до мягкости.'),
                ('Шпинат', 'Добавьте шпинат и готовьте 1–2 минуты, пока он не осядет.'),
                ('Яичная смесь', 'Взбейте яйца с молоком и солью, добавьте тёртый сыр.'),
                ('Запекание', 'Вылейте смесь на сковороду и запекайте 8–10 минут.'),
                ('Подача', 'Нарежьте фриттату порциями и подавайте тёплой.')
            ]
        },
        {
            'title': 'Тыквенные панкейки',
            'description': 'Воздушные панкейки с тыквой и пряностями.',
            'cooking_time': 25,
            'difficulty': Difficulty.EASY,
            'image_query': 'pumpkin pancakes',
            'categories': ['Выпечка', 'Завтраки'],
            'ingredients': ['тыква', 'мука', 'яйца', 'молоко', 'разрыхлитель', 'сахар', 'корица'],
            'steps': [
                ('Тыквенное пюре', 'Запеките тыкву и разомните до пюре.'),
                ('Сухие ингредиенты', 'Смешайте муку, разрыхлитель, сахар и корицу.'),
                ('Жидкие ингредиенты', 'Взбейте яйца с молоком и добавьте тыквенное пюре.'),
                ('Тесто', 'Соедините сухие и жидкие ингредиенты до густого теста.'),
                ('Жарка', 'Выпекайте панкейки на сухой сковороде по 2–3 минуты с каждой стороны.'),
                ('Подача', 'Подавайте с мёдом или ягодами.')
            ]
        },
        {
            'title': 'Банановый смузи',
            'description': 'Освежающий смузи с бананом и йогуртом.',
            'cooking_time': 10,
            'difficulty': Difficulty.EASY,
            'image_query': 'banana smoothie',
            'categories': ['Напитки'],
            'ingredients': ['банан', 'йогурт', 'молоко', 'мёд', 'клубника'],
            'steps': [
                ('Подготовка фруктов', 'Нарежьте банан ломтиками и подготовьте ягоды.'),
                ('Смешивание', 'Положите банан и клубнику в блендер.'),
                ('Жидкая основа', 'Добавьте йогурт и молоко.'),
                ('Сладость', 'Влейте мёд и взбейте 30 секунд.'),
                ('Проверка', 'Отрегулируйте густоту, добавив ещё молока при необходимости.'),
                ('Подача', 'Разлейте смузи по стаканам и сразу подавайте.')
            ]
        },
        {
            'title': 'Чиа-пудинг с ягодами',
            'description': 'Лёгкий десерт на основе семян чиа и ягод.',
            'cooking_time': 15,
            'difficulty': Difficulty.EASY,
            'image_query': 'chia pudding',
            'categories': ['Десерты'],
            'ingredients': ['семена чиа', 'молоко', 'мёд', 'черника', 'малина', 'ваниль'],
            'steps': [
                ('Смешивание', 'Соедините молоко, семена чиа, мёд и ваниль.'),
                ('Перемешивание', 'Тщательно размешайте, чтобы не было комков.'),
                ('Набухание', 'Оставьте смесь на 10 минут и снова перемешайте.'),
                ('Охлаждение', 'Поставьте в холодильник минимум на 2 часа.'),
                ('Сборка', 'Разложите пудинг по стаканам.'),
                ('Подача', 'Добавьте свежие ягоды перед подачей.')
            ]
        },
        {
            'title': 'Шоколадный брауни',
            'description': 'Плотный шоколадный брауни с насыщенным вкусом какао.',
            'cooking_time': 40,
            'difficulty': Difficulty.MEDIUM,
            'image_query': 'brownie',
            'categories': ['Выпечка', 'Десерты'],
            'ingredients': ['мука', 'какао', 'шоколад', 'яйца', 'сливочное масло', 'сахар'],
            'steps': [
                ('Разогрев', 'Разогрейте духовку до 180°C и подготовьте форму.'),
                ('Растапливание', 'Растопите шоколад со сливочным маслом на водяной бане.'),
                ('Яичная смесь', 'Взбейте яйца с сахаром до лёгкой пены.'),
                ('Соединение', 'Смешайте шоколадную массу с яйцами.'),
                ('Сухие ингредиенты', 'Просейте муку и какао, аккуратно вмешайте.'),
                ('Выпекание', 'Вылейте тесто в форму и выпекайте 20–25 минут.'),
                ('Остывание', 'Остудите брауни и нарежьте квадратами.')
            ]
        },
        {
            'title': 'Сырники со сметаной',
            'description': 'Классические сырники с румяной корочкой.',
            'cooking_time': 25,
            'difficulty': Difficulty.EASY,
            'image_query': 'cheesecakes',
            'categories': ['Десерты', 'Завтраки'],
            'ingredients': ['творог', 'яйца', 'мука', 'сахар', 'сметана', 'ваниль'],
            'steps': [
                ('Тесто', 'Смешайте творог, яйца, сахар и ваниль до однородности.'),
                ('Мука', 'Добавьте муку и аккуратно перемешайте.'),
                ('Формование', 'Сформируйте небольшие сырники и обваляйте в муке.'),
                ('Разогрев', 'Разогрейте сковороду с небольшим количеством масла.'),
                ('Жарка', 'Обжарьте по 2–3 минуты с каждой стороны до золотистого цвета.'),
                ('Подача', 'Подавайте горячими со сметаной.')
            ]
        },
        {
            'title': 'Плов с говядиной',
            'description': 'Ароматный плов с говядиной и специями.',
            'cooking_time': 60,
            'difficulty': Difficulty.MEDIUM,
            'image_query': 'beef pilaf',
            'categories': ['Обеды', 'Мясо'],
            'ingredients': ['говядина', 'рис', 'морковь', 'лук', 'чеснок', 'паприка', 'соль'],
            'steps': [
                ('Подготовка мяса', 'Нарежьте говядину кусочками и обжарьте до румяности.'),
                ('Овощи', 'Добавьте лук и морковь, готовьте 5–6 минут.'),
                ('Специи', 'Всыпьте паприку и соль, перемешайте.'),
                ('Добавление риса', 'Промойте рис и выложите поверх мяса и овощей.'),
                ('Вода', 'Залейте горячей водой так, чтобы покрыть рис на 1,5 см.'),
                ('Томление', 'Тушите на слабом огне 20–25 минут под крышкой.'),
                ('Отдых', 'Снимите с огня и дайте плову настояться 10 минут.')
            ]
        },
        {
            'title': 'Суп минестроне',
            'description': 'Итальянский овощной суп с фасолью и зеленью.',
            'cooking_time': 40,
            'difficulty': Difficulty.EASY,
            'image_query': 'minestrone soup',
            'categories': ['Супы'],
            'ingredients': ['фасоль', 'морковь', 'лук', 'сельдерей', 'помидоры', 'чеснок', 'оливковое масло', 'базилик'],
            'steps': [
                ('Подготовка овощей', 'Нарежьте морковь, лук и сельдерей мелким кубиком.'),
                ('Обжарка', 'Обжарьте овощи на масле 4–5 минут.'),
                ('Томаты', 'Добавьте нарезанные помидоры и готовьте ещё 3 минуты.'),
                ('Вода', 'Влейте воду и доведите до кипения.'),
                ('Фасоль', 'Добавьте фасоль и варите 15 минут на среднем огне.'),
                ('Аромат', 'Добавьте чеснок и базилик, посолите.'),
                ('Подача', 'Дайте супу настояться 5 минут перед подачей.')
            ]
        },
        {
            'title': 'Куриное филе на гриле',
            'description': 'Нежное куриное филе с лимоном и паприкой.',
            'cooking_time': 25,
            'difficulty': Difficulty.EASY,
            'image_query': 'grilled chicken breast',
            'categories': ['Ужины', 'Мясо'],
            'ingredients': ['курица', 'лимон', 'паприка', 'оливковое масло', 'чеснок', 'соль'],
            'steps': [
                ('Маринад', 'Смешайте масло, лимонный сок, паприку и чеснок.'),
                ('Маринование', 'Смажьте филе маринадом и оставьте на 10 минут.'),
                ('Разогрев', 'Разогрейте гриль или сковороду-гриль.'),
                ('Готовка', 'Готовьте филе по 4–5 минут с каждой стороны.'),
                ('Отдых', 'Дайте мясу отдохнуть 3 минуты перед нарезкой.'),
                ('Подача', 'Нарежьте ломтиками и подавайте с салатом.')
            ]
        },
        {
            'title': 'Салат с печёной свеклой и козьим сыром',
            'description': 'Салат с карамельной свёклой, орехами и мягким сыром.',
            'cooking_time': 40,
            'difficulty': Difficulty.EASY,
            'image_query': 'beet salad',
            'categories': ['Салаты'],
            'ingredients': ['свекла', 'сыр', 'руккола', 'орехи', 'мёд', 'оливковое масло', 'соль'],
            'steps': [
                ('Запекание свёклы', 'Заверните свёклу в фольгу и запеките при 200°C 30–35 минут.'),
                ('Охлаждение', 'Остудите свёклу и нарежьте ломтиками.'),
                ('Заправка', 'Смешайте масло, мёд и щепотку соли.'),
                ('Основа', 'Разложите рукколу, добавьте ломтики свёклы.'),
                ('Сыр и орехи', 'Добавьте кусочки сыра и измельчённые орехи.'),
                ('Подача', 'Полейте заправкой и подавайте.')
            ]
        },
        {
            'title': 'Ризотто с грибами',
            'description': 'Кремовое ризотто с грибами и сыром.',
            'cooking_time': 35,
            'difficulty': Difficulty.MEDIUM,
            'image_query': 'mushroom risotto',
            'categories': ['Обеды', 'Паста'],
            'ingredients': ['рис', 'грибы', 'лук', 'сыр', 'сливки', 'сливочное масло', 'соль'],
            'steps': [
                ('Подготовка', 'Обжарьте лук на масле до прозрачности.'),
                ('Грибы', 'Добавьте грибы и готовьте 5 минут до мягкости.'),
                ('Рис', 'Всыпьте рис и обжарьте 1 минуту, чтобы он стал прозрачным.'),
                ('Сливки', 'Постепенно добавляйте сливки и немного воды, помешивая.'),
                ('Готовность', 'Готовьте 15–18 минут до кремовой текстуры.'),
                ('Сыр', 'Добавьте тёртый сыр, посолите и перемешайте перед подачей.')
            ]
        },
        {
            'title': 'Овощной рататуй',
            'description': 'Французский рататуй с томатами и прованскими травами.',
            'cooking_time': 45,
            'difficulty': Difficulty.MEDIUM,
            'image_query': 'ratatouille',
            'categories': ['Вегетарианские', 'Ужины'],
            'ingredients': ['баклажаны', 'кабачки', 'помидоры', 'лук', 'чеснок', 'оливковое масло', 'розмарин', 'соль'],
            'steps': [
                ('Подготовка', 'Нарежьте баклажаны, кабачки и помидоры тонкими кружками.'),
                ('Соус', 'Обжарьте лук с чесноком, добавьте часть помидоров и тушите 5 минут.'),
                ('Сборка', 'Выложите соус в форму и уложите овощи слоями.'),
                ('Приправы', 'Посолите и добавьте розмарин, сбрызните маслом.'),
                ('Запекание', 'Запекайте при 180°C 30–35 минут.'),
                ('Подача', 'Дайте рататую постоять 5 минут перед подачей.')
            ]
        }
    ]

    recipes_to_create = 0
    recipes_updated = 0

    for data in recipes_data:
        title = data['title']
        normalized_title = normalize_name(title)
        recipe = existing_recipes.get(normalized_title)

        ingredients = []
        for name in data['ingredients']:
            ing = get_ingredient(name)
            if ing:
                ingredients.append(ing)

        categories = []
        for name in data['categories']:
            cat = get_category(name)
            if cat:
                categories.append(cat)

        if recipe:
            recipe.description = data['description']
            recipe.cooking_time = data['cooking_time']
            recipe.difficulty = data['difficulty']
            recipe.image_url = recipe_image_url(data['image_query'])
            recipe.ingredients = ingredients
            recipe.categories = categories

            if recipe.learning:
                learning = recipe.learning
                learning.title = f"Как приготовить {title.lower()}"
                learning.steps = []
            else:
                learning = Learning(title=f"Как приготовить {title.lower()}", recipe=recipe)
                recipe.learning = learning

            learning.steps = [
                StepLearning(
                    title=step_title,
                    description=step_desc,
                    number=idx + 1,
                    learning=learning
                )
                for idx, (step_title, step_desc) in enumerate(data['steps'])
            ]
            recipes_updated += 1
        else:
            recipe = Recipe(
                title=title,
                description=data['description'],
                cooking_time=data['cooking_time'],
                difficulty=data['difficulty'],
                image_url=recipe_image_url(data['image_query'])
            )
            recipe.ingredients = ingredients
            recipe.categories = categories
            learning = Learning(title=f"Как приготовить {title.lower()}", recipe=recipe)
            learning.steps = [
                StepLearning(
                    title=step_title,
                    description=step_desc,
                    number=idx + 1,
                    learning=learning
                )
                for idx, (step_title, step_desc) in enumerate(data['steps'])
            ]
            recipe.learning = learning
            db.session.add(recipe)
            recipes_to_create += 1

    db.session.commit()
    print(f"✓ Recipes: {recipes_to_create} added, {recipes_updated} updated")

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
