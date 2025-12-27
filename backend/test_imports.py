#!/usr/bin/env python
"""
Smoke test для проверки импортов моделей.
Использование: python test_imports.py
"""
try:
    from models import Recipe, Difficulty, Mark, Consumer, Ingredient, Category, Comment
    print("✓ Все основные модели импортированы успешно")
    
    # Проверяем, что Difficulty - это Enum
    assert Difficulty.EASY.value == 'easy'
    assert Difficulty.MEDIUM.value == 'medium'
    assert Difficulty.HARD.value == 'hard'
    print("✓ Difficulty enum работает корректно")
    
    print("\n✅ Все импорты работают!")
    exit(0)
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    exit(1)
except AssertionError as e:
    print(f"❌ Ошибка проверки: {e}")
    exit(1)

