#!/usr/bin/env python3
"""Generate seed images for categories, recipes, and ingredients.

Usage:
    python scripts/fetch_images.py
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = REPO_ROOT / "backend" / "static" / "img"

CATEGORIES = [
    'Завтраки', 'Обеды', 'Ужины', 'Десерты', 'Салаты', 'Супы', 'Выпечка',
    'Напитки', 'Закуски', 'Вегетарианские', 'Мясо', 'Паста', 'Все блюда'
]

RECIPES = [
    'Омлет с овощами',
    'Овсяная каша с ягодами',
    'Тыквенный крем-суп',
    'Курица терияки с рисом',
    'Паста карбонара',
    'Салат Цезарь',
    'Греческий салат',
    'Борщ домашний',
    'Рагу из овощей',
    'Запечённый лосось с лимоном',
    'Картофельное пюре с грибами',
    'Котлеты из индейки',
    'Тёплый салат с креветками',
    'Овощная паста с томатами',
    'Фриттата со шпинатом',
    'Тыквенные панкейки',
    'Банановый смузи',
    'Чиа-пудинг с ягодами',
    'Шоколадный брауни',
    'Сырники со сметаной',
    'Плов с говядиной',
    'Суп минестроне',
    'Куриное филе на гриле',
    'Салат с печёной свеклой и козьим сыром',
    'Ризотто с грибами',
    'Овощной рататуй',
    'Свинина с овощами на сковороде',
    'Тушёная баранина с картофелем',
    'Кролик в сметанном соусе',
    'Рыбные котлеты',
    'Салат с тунцом и яйцом',
    'Треска с лимоном в духовке',
    'Кальмар в сливочно-чесночном соусе'
]

INGREDIENTS = [
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

PALETTE = [
    (109, 40, 217),
    (147, 51, 234),
    (245, 158, 11),
    (16, 163, 74),
    (14, 116, 144),
    (239, 68, 68),
    (99, 102, 241),
    (244, 63, 94),
]


def normalize_name(value: str) -> str:
    if not value:
        return ''
    normalized = re.sub(r'\s+', ' ', value.strip().lower())
    return normalized


def slugify(value: str) -> str:
    if not value:
        return ''
    translit_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    normalized = unicodedata.normalize('NFKD', value).lower().replace('ё', 'е')
    normalized = ''.join(
        char for char in normalized if unicodedata.category(char) != 'Mn'
    )
    slug_chars = []
    for char in normalized:
        if char.isalnum():
            slug_chars.append(translit_map.get(char, char))
        else:
            slug_chars.append('-')
    slug = re.sub(r'-{2,}', '-', ''.join(slug_chars))
    return slug.strip('-')


def dedupe(names: list[str]) -> list[str]:
    seen = set()
    unique = []
    for name in names:
        normalized = normalize_name(name).replace('ё', 'е')
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique.append(name)
    return unique


def pick_colors(seed: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    total = sum(ord(char) for char in seed)
    first = PALETTE[total % len(PALETTE)]
    second = PALETTE[(total + 3) % len(PALETTE)]
    return first, second


def svg_template(width: int, height: int, title: str, seed: str) -> str:
    primary, secondary = pick_colors(seed)
    font_size = 32 if width >= 800 else 26
    return f"""
<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\">
  <defs>
    <linearGradient id=\"grad\" x1=\"0%\" y1=\"0%\" x2=\"100%\" y2=\"100%\">
      <stop offset=\"0%\" stop-color=\"rgb{primary}\" />
      <stop offset=\"100%\" stop-color=\"rgb{secondary}\" />
    </linearGradient>
  </defs>
  <rect width=\"{width}\" height=\"{height}\" fill=\"url(#grad)\" />
  <rect x=\"24\" y=\"24\" width=\"{width - 48}\" height=\"{height - 48}\" rx=\"28\" fill=\"rgba(255,255,255,0.15)\" />
  <text x=\"50%\" y=\"50%\" text-anchor=\"middle\" dominant-baseline=\"middle\" fill=\"#fff\" font-family=\"Segoe UI, Arial, sans-serif\" font-size=\"{font_size}\" font-weight=\"600\">{title}</text>
</svg>
""".strip()


def write_svg(destination: Path, width: int, height: int, title: str) -> None:
    if destination.exists():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    seed = destination.stem
    destination.write_text(svg_template(width, height, title, seed), encoding="utf-8")


def render_group(kind: str, names: list[str], width: int, height: int) -> None:
    for name in names:
        slug = slugify(name)
        destination = OUTPUT_ROOT / kind / f"{slug}.svg"
        write_svg(destination, width, height, name)


def main() -> None:
    render_group('categories', CATEGORIES, 960, 640)
    render_group('recipes', RECIPES, 960, 640)
    render_group('ingredients', dedupe(INGREDIENTS), 600, 600)


if __name__ == '__main__':
    main()
