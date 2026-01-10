# Recipe Finder

Полнофункциональное веб-приложение для поиска рецептов по ингредиентам с поддержкой авторизации, избранного, истории просмотров, комментариев и оценок.

## Технологический стек

### Backend
- Python 3.11+
- Flask
- SQLAlchemy ORM
- Alembic (миграции)
- PostgreSQL
- JWT (авторизация)
- Werkzeug (хеширование паролей)

### Frontend
- HTML/CSS/Vanilla JavaScript
- Адаптивная верстка (mobile-first)

### Инфраструктура
- Docker & Docker Compose
- PostgreSQL

## Структура проекта

```
SmartCook/
├── backend/
│   ├── api/              # REST API endpoints
│   │   ├── auth_routes.py
│   │   ├── recipe_routes.py
│   │   ├── ingredient_routes.py
│   │   ├── category_routes.py
│   │   ├── comment_routes.py
│   │   ├── mark_routes.py
│   │   ├── admin_routes.py
│   │   └── middleware.py
│   ├── models/           # SQLAlchemy модели
│   ├── repository/       # Слой доступа к данным
│   ├── service/          # Бизнес-логика
│   ├── exception/        # Обработка ошибок
│   ├── tests/            # Тесты
│   ├── config.py
│   ├── extensions.py
│   ├── run.py
│   ├── seed.py           # Скрипт загрузки данных
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── js/
│   │   └── api.js        # API клиент
│   ├── css/
│   │   └── common.css   # Общие стили
│   └── *.html           # Страницы приложения
├── docker-compose.yml
└── README.md
```

## Установка и запуск

### Требования
- Docker и Docker Compose
- Или Python 3.11+ и PostgreSQL (для локальной разработки)

## Все правила запуска вы найдёте в файле QUICKSTART.md

### Запуск с Docker

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd SmartCook
```

2. При необходимости настройте переменные окружения (для Docker можно создать `.env` в корне проекта):
```env
JWT_SECRET_KEY=your-secret-key-change-in-production
# Опционально (для локальной разработки без Docker)
DATABASE_URL=postgresql://smartcook:smartcook_pass@localhost:5432/smartcook_db
CORS_ORIGINS=http://localhost:8080,http://127.0.0.1:8080
SECRET_KEY=dev-secret-key
```

3. Запустите приложение:
```bash
# Для чистого старта (удалит все данные, если нужно начать заново):
# docker-compose down -v

docker-compose up --build --force-recreate
```

**Примечание:** Если нужно полностью пересоздать базу данных с нуля, используйте `docker-compose down -v` перед запуском (это удалит все данные).

4. Загрузите начальные данные:
```bash
# Обычный режим: добавить недостающие данные (идемпотентный)
docker-compose exec backend python seed.py

# Режим сброса: очистить и загрузить заново
docker-compose exec backend python seed.py --reset
```

**Примечание:** `seed.py` идемпотентен - его можно запускать многократно без ошибок. Он автоматически пропускает уже существующие данные и добавляет только новые. Используйте `--reset` только если нужно полностью пересоздать начальные данные.

5. Откройте в браузере:
- Backend API (Docker): http://localhost:5001
- Frontend: откройте `frontend/index.html` в браузере или используйте простой HTTP сервер:
```bash
cd frontend
python -m http.server 8080
```

### Генерация локальных изображений

Все изображения для категорий, рецептов и ингредиентов хранятся локально и используются из seed-данных.
Для пересоздания набора изображений запустите:

```bash
python scripts/fetch_images.py
```

Скрипт идемпотентный: если файл уже существует, он не будет перезаписан.

### Локальная разработка

1. Установите зависимости:
```bash
cd backend
pip install -r requirements.txt
```

2. Настройте PostgreSQL и создайте базу данных:
```sql
CREATE DATABASE smartcook_db;
CREATE USER smartcook WITH PASSWORD 'smartcook_pass';
GRANT ALL PRIVILEGES ON DATABASE smartcook_db TO smartcook;
```

3. Создайте `.env` файл (см. выше, но используйте `localhost` вместо `db`)

4. Запустите миграции:
```bash
flask db upgrade
```

5. Загрузите данные:
```bash
python seed.py
```

6. Запустите сервер:
```bash
python run.py
```

## Переменные окружения

- `DATABASE_URL` - URL подключения к PostgreSQL
- `JWT_SECRET_KEY` - Секретный ключ для JWT токенов
- `CORS_ORIGINS` - Разрешённые источники для CORS (через запятую)
- `FLASK_ENV` - Окружение Flask (development/production)
- `SECRET_KEY` - Секретный ключ Flask (для подписи cookies)

## Проверка подключения к базе данных

После запуска `docker-compose up` можно проверить подключение к базе данных:

```bash
# Проверка через psql
docker-compose exec db psql -U smartcook -d smartcook_db -c "SELECT 1"

# Проверка healthcheck
docker-compose ps db

# Просмотр логов базы данных
docker-compose logs db
```

Если в логах появляются ошибки `FATAL: database "smartcook" does not exist`, убедитесь, что:
1. Используется `docker-compose up --build --force-recreate` для пересоздания контейнеров
2. Healthcheck в `docker-compose.yml` содержит `-d smartcook_db`
3. Переменная `POSTGRES_DB=smartcook_db` установлена в окружении контейнера db

## API Endpoints

### Авторизация
- `POST /api/auth/register` - Регистрация
- `POST /api/auth/login` - Вход
- `GET /api/me` - Профиль пользователя
- `PUT /api/me` - Обновление профиля
- `POST /api/me/avatar` - Загрузка аватара (multipart/form-data)
- `GET /api/me/forbidden-ingredients` - Запрещённые ингредиенты
- `PUT /api/me/forbidden-ingredients` - Обновление запрещённых ингредиентов

### Рецепты
- `GET /api/recipes` - Поиск рецептов (query params: q, ingredients, minMatch, maxTime, difficulty, categoryId, sort)
- `GET /api/recipes/{id}` - Детали рецепта
- `GET /api/recipes/{id}/missing` - Отсутствующие ингредиенты
- `GET /api/recommendations` - Рекомендации (требует авторизации)

### Избранное
- `GET /api/favourites` - Список избранного
- `POST /api/favourites` - Добавить в избранное
- `DELETE /api/favourites/{recipe_id}` - Удалить из избранного

### История
- `GET /api/history` - История просмотров
- `POST /api/history` - Добавить в историю

### Ингредиенты и категории
- `GET /api/ingredients` - Список ингредиентов (query: q)
- `GET /api/categories` - Список категорий

### Комментарии
- `GET /api/recipes/{id}/comments` - Комментарии к рецепту
- `POST /api/recipes/{id}/comments` - Создать комментарий
- `DELETE /api/comments/{id}` - Удалить комментарий

### Оценки
- `POST /api/recipes/{id}/mark` - Поставить оценку (1-5)
- `DELETE /api/recipes/{id}/mark` - Удалить свою оценку
- `GET /api/me/marks` - Мои оценки

### Админ-панель (требует роль admin)
- `GET /api/admin/recipes` - Список всех рецептов
- `POST /api/admin/recipes` - Создать рецепт
- `PUT /api/admin/recipes/{id}` - Обновить рецепт
- `DELETE /api/admin/recipes/{id}` - Удалить рецепт
- `DELETE /api/admin/comments/{id}` - Удалить комментарий
- `POST /api/admin/categories` - Создать категорию
- `POST /api/admin/ingredients` - Создать ингредиент

## Алгоритм поиска рецептов

1. Исключаются рецепты с запрещёнными ингредиентами пользователя
2. Для каждого рецепта вычисляется:
   - `match_percent` = (совпадающие ингредиенты / всего ингредиентов)
   - `missing_ingredients` = ингредиенты рецепта, которых нет у пользователя
3. Фильтрация по минимальному `match_percent` (по умолчанию > 0)
4. Сортировка: по `match_percent` (desc), затем по рейтингу (desc), затем по времени (asc)
5. Применяются дополнительные фильтры: время, сложность, категория

## Тестирование

Запуск тестов:
```bash
cd backend
pytest
```

Тесты покрывают:
- Авторизацию (регистрация, вход, JWT)
- API endpoints (smoke тесты)
- Базовую функциональность поиска

## Данные по умолчанию

После выполнения `seed.py` создаётся:
- Администратор: `admin@example.com` / `Admin123!`
- Базовые ингредиенты (115 уникальных, дубликаты автоматически удаляются)
- Категории (13 штук)
- Демо-рецепты (33 штуки)

**Идемпотентность:** `seed.py` можно запускать многократно - он автоматически:
- Пропускает уже существующие ингредиенты, категории, роли
- Не создаёт дубликаты (нормализация имён: strip, lower, удаление множественных пробелов)
- Показывает статистику: сколько добавлено, сколько пропущено
- Поддерживает флаг `--reset` для полной очистки и пересоздания данных

## Особенности реализации

### Безопасность
- Пароли хешируются с использованием Werkzeug
- JWT токены с истечением срока действия
- Защита admin endpoints по роли
- CORS настроен для фронтенда

### Производительность
- Избегание N+1 запросов через join и агрегацию
- Индексы на ключевых полях
- Оптимизированные запросы для поиска

### Архитектура
- Слоистая архитектура: API → Service → Repository → Model
- Разделение ответственности
- Обработка ошибок через единый формат

## Проверка CORS

После запуска приложения можно проверить, что CORS настроен корректно:

### A) Preflight запрос (OPTIONS) - проверка регистрации
```bash
curl -i -X OPTIONS http://localhost:5001/api/auth/register \
  -H "Origin: http://localhost:8080" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: content-type"
```

**Ожидаемый результат:** В ответе должны быть заголовки:
- `Access-Control-Allow-Origin: http://localhost:8080`
- `Access-Control-Allow-Methods: GET,POST,PUT,PATCH,DELETE,OPTIONS`
- `Access-Control-Allow-Headers: Content-Type,Authorization`
- HTTP статус: `200` или `204`

**Если получаете 403:** Проверьте:
1. Что `CORS_ORIGINS` в docker-compose.yml включает ваш origin
2. Что Flask-CORS правильно инициализирован в `run.py`
3. Логи backend: `docker-compose logs backend | grep OPTIONS`

### B) POST запрос регистрации с CORS заголовками
```bash
curl -i -X POST http://localhost:5001/api/auth/register \
  -H "Origin: http://localhost:8080" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'
```

**Ожидаемый результат:** В ответе должен быть заголовок:
- `Access-Control-Allow-Origin: http://localhost:8080`
- HTTP статус: `201 CREATED`
- JSON с `access_token` и `consumer`

### Отладка CORS проблем

Если в браузере видите "Preflight response is not successful. Status code: 403":

1. **Проверьте логи backend:**
   ```bash
   docker-compose logs backend | tail -20
   ```
   Должны видеть логи вида: `OPTIONS /api/auth/register - Origin: http://localhost:8080`

2. **Проверьте переменную окружения:**
   ```bash
   docker-compose exec backend env | grep CORS_ORIGINS
   ```

3. **Проверьте, что origin в списке разрешённых:**
   - Откройте DevTools → Network → выберите failed request
   - Проверьте заголовок `Origin` в запросе
   - Убедитесь, что он точно совпадает с одним из значений в `CORS_ORIGINS`

## Примеры запросов

### Регистрация
```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"user","email":"user@example.com","password":"password123"}'
```

### Вход
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"emailOrPhone":"user@example.com","password":"password123"}'
```

### Поиск рецептов
```bash
curl "http://localhost:5001/api/recipes?ingredients=курица,картофель&minMatch=0.3&sort=match"
```

### Создание комментария (требует токен)
```bash
curl -X POST http://localhost:5001/api/recipes/1/comments \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"Отличный рецепт!"}'
```

## Лицензия

MIT
