# Проверка импортов

## Проблема
`ImportError: cannot import name 'Difficulty' from 'models'`

## Решение
Добавлен экспорт `Difficulty` в `models/__init__.py`:
```python
from .recipe import Recipe, Difficulty
```

## Проверка

### Внутри контейнера:
```bash
docker-compose exec backend python -c "from models import Recipe, Difficulty, Mark; print('OK')"
```

### Или запустить тест:
```bash
docker-compose exec backend python test_imports.py
```

### Проверка запуска приложения:
```bash
docker-compose exec backend python -c "from run import create_app; app = create_app(); print('App created successfully')"
```

