import { BASE_URL } from './api.js';

export const PLACEHOLDER_IMAGE = '/static/img/placeholder.svg';

export function normalizeKey(name) {
    if (!name) {
        return '';
    }
    return name
        .trim()
        .toLowerCase()
        .replace(/ё/g, 'е')
        .replace(/["'`’“”.,:;!?()\[\]{}<>«»\/\\]/g, '')
        .replace(/\s+/g, ' ');
}

const CATEGORY_IMAGES = {
    'завтраки': 'https://source.unsplash.com/960x640/?breakfast,food',
    'обеды': 'https://source.unsplash.com/960x640/?lunch,food',
    'ужины': 'https://source.unsplash.com/960x640/?dinner,food',
    'десерты': 'https://source.unsplash.com/960x640/?dessert,food',
    'салаты': 'https://source.unsplash.com/960x640/?salad,food',
    'супы': 'https://source.unsplash.com/960x640/?soup,food',
    'выпечка': 'https://source.unsplash.com/960x640/?baking,food',
    'напитки': 'https://source.unsplash.com/960x640/?drinks,beverage',
    'закуски': 'https://source.unsplash.com/960x640/?appetizer,food',
    'вегетарианские': 'https://source.unsplash.com/960x640/?vegetarian,food',
    'мясо': 'https://source.unsplash.com/960x640/?meat,food',
    'паста': 'https://source.unsplash.com/960x640/?pasta,food',
    'все блюда': 'https://source.unsplash.com/960x640/?food,meal'
};

const RECIPE_IMAGES = {
    'овсяная каша': 'https://source.unsplash.com/960x640/?oatmeal,breakfast',
    'сырники': 'https://source.unsplash.com/960x640/?cheesecakes,food',
    'омлет': 'https://source.unsplash.com/960x640/?omelette,food',
    'панкейки': 'https://source.unsplash.com/960x640/?pancakes,food',
    'суп': 'https://source.unsplash.com/960x640/?soup,food',
    'салат': 'https://source.unsplash.com/960x640/?salad,food',
    'паста': 'https://source.unsplash.com/960x640/?pasta,food',
    'курица': 'https://source.unsplash.com/960x640/?chicken,food',
    'рыба': 'https://source.unsplash.com/960x640/?fish,food',
    'десерт': 'https://source.unsplash.com/960x640/?dessert,food'
};

const INGREDIENT_IMAGES = {
    'курица': 'https://source.unsplash.com/600x600/?chicken,raw',
    'индейка': 'https://source.unsplash.com/600x600/?turkey,meat',
    'говядина': 'https://source.unsplash.com/600x600/?beef,meat',
    'свинина': 'https://source.unsplash.com/600x600/?pork,meat',
    'баранина': 'https://source.unsplash.com/600x600/?lamb,meat',
    'кролик': 'https://source.unsplash.com/600x600/?rabbit,meat',
    'рыба': 'https://source.unsplash.com/600x600/?fish,food',
    'лосось': 'https://source.unsplash.com/600x600/?salmon,fish',
    'тунец': 'https://source.unsplash.com/600x600/?tuna,fish',
    'треска': 'https://source.unsplash.com/600x600/?cod,fish',
    'креветки': 'https://source.unsplash.com/600x600/?shrimp,seafood',
    'кальмар': 'https://source.unsplash.com/600x600/?squid,seafood',
    'лук': 'https://source.unsplash.com/600x600/?onion,vegetable',
    'чеснок': 'https://source.unsplash.com/600x600/?garlic,food',
    'картофель': 'https://source.unsplash.com/600x600/?potato,vegetable',
    'морковь': 'https://source.unsplash.com/600x600/?carrot,vegetable',
    'помидоры': 'https://source.unsplash.com/600x600/?tomato,vegetable',
    'огурцы': 'https://source.unsplash.com/600x600/?cucumber,vegetable',
    'яйца': 'https://source.unsplash.com/600x600/?eggs,food',
    'молоко': 'https://source.unsplash.com/600x600/?milk,food',
    'сыр': 'https://source.unsplash.com/600x600/?cheese,food',
    'рис': 'https://source.unsplash.com/600x600/?rice,grain',
    'гречка': 'https://source.unsplash.com/600x600/?buckwheat,grain',
    'мука': 'https://source.unsplash.com/600x600/?flour,baking',
    'масло': 'https://source.unsplash.com/600x600/?butter,food',
    'сливочное масло': 'https://source.unsplash.com/600x600/?butter,food'
};

const LOCAL_PLACEHOLDER_PATHS = ['/static/img/ingredients/', '/static/img/recipes/', '/static/img/categories/'];

function isPlaceholderAsset(url) {
    if (!url) return true;
    return LOCAL_PLACEHOLDER_PATHS.some(path => url.includes(path));
}

function findMappedImage(map, normalized) {
    if (map[normalized]) {
        return map[normalized];
    }
    const entry = Object.entries(map).find(([key]) => normalized.includes(key));
    return entry ? entry[1] : '';
}

export function getImageForName(name, type = 'recipe') {
    const normalized = normalizeKey(name);
    if (!normalized) {
        return '';
    }

    if (type === 'category') {
        return findMappedImage(CATEGORY_IMAGES, normalized) || `https://source.unsplash.com/960x640/?${encodeURIComponent(`${normalized} food`)}`;
    }

    if (type === 'ingredient' || type === 'product') {
        return findMappedImage(INGREDIENT_IMAGES, normalized) || `https://source.unsplash.com/600x600/?${encodeURIComponent(`${normalized} ingredient`)}`;
    }

    return findMappedImage(RECIPE_IMAGES, normalized) || `https://source.unsplash.com/960x640/?${encodeURIComponent(`${normalized} dish`)}`;
}

export function normalizeImageUrl(url) {
    if (!url) {
        return PLACEHOLDER_IMAGE;
    }

    if (url.startsWith('data:') || url.startsWith('blob:')) {
        return url;
    }

    if (url.startsWith('http://') || url.startsWith('https://')) {
        return url;
    }

    const normalizedPath = url.startsWith('/') ? url : `/${url}`;
    return `${BASE_URL}${normalizedPath}`;
}

export function setImageWithFallback(imgEl, url) {
    if (!imgEl) return;

    const providedUrl = url || '';
    const name = imgEl.dataset.imageName || imgEl.getAttribute('alt') || '';
    const type = imgEl.dataset.imageType || 'recipe';
    const shouldReplace = isPlaceholderAsset(providedUrl);
    const resolvedUrl = shouldReplace ? getImageForName(name, type) : (providedUrl || getImageForName(name, type));

    imgEl.dataset.imageUrl = resolvedUrl;
    imgEl.onerror = () => {
        if (imgEl.dataset.fallbackApplied === 'true') {
            return;
        }
        imgEl.dataset.fallbackApplied = 'true';
        imgEl.src = PLACEHOLDER_IMAGE;
    };

    imgEl.src = normalizeImageUrl(resolvedUrl);
}

export function applyImageFallbacks(container) {
    if (!container) return;
    container.querySelectorAll('img[data-image-url]').forEach((img) => {
        setImageWithFallback(img, img.dataset.imageUrl);
    });
}
