import { BASE_URL } from './api.js';

export const PLACEHOLDER_IMAGE = '/static/img/placeholder.svg';
const CATEGORY_IMAGES = {
    'завтраки': '/static/img/categories/breakfasts.svg',
    'обеды': '/static/img/categories/pasta.svg',
    'ужины': '/static/img/categories/meat.svg',
    'десерты': '/static/img/categories/desserts.svg',
    'салаты': '/static/img/categories/salads.svg',
    'супы': '/static/img/categories/soups.svg',
    'выпечка': '/static/img/categories/pasta.svg',
    'напитки': '/static/img/categories/drinks.svg',
    'закуски': '/static/img/categories/all.svg',
    'вегетарианские': '/static/img/categories/salads.svg',
    'мясо': '/static/img/categories/meat.svg',
    'паста': '/static/img/categories/pasta.svg',
    'все блюда': '/static/img/categories/all.svg'
};

const RECIPE_IMAGES = Array.from({ length: 24 }, (_, index) => {
    const slot = String(index + 1).padStart(2, '0');
    return `/static/img/recipes/recipe-${slot}.svg`;
});

const INGREDIENT_IMAGES = Array.from({ length: 24 }, (_, index) => {
    const slot = String(index + 1).padStart(2, '0');
    return `/static/img/ingredients/ingredient-${slot}.svg`;
});

function normalizeName(name) {
    if (!name) {
        return '';
    }
    return name
        .trim()
        .toLowerCase()
        .replace(/ё/g, 'е')
        .replace(/\s+/g, ' ');
}

function hashString(value) {
    let hash = 0;
    for (let i = 0; i < value.length; i += 1) {
        hash = (hash << 5) - hash + value.charCodeAt(i);
        hash |= 0;
    }
    return Math.abs(hash);
}

export function getImageForName(name, type = 'recipe') {
    const normalized = normalizeName(name);
    if (!normalized) {
        return '';
    }

    if (type === 'category') {
        return CATEGORY_IMAGES[normalized] || `https://source.unsplash.com/800x600/?${encodeURIComponent(`${normalized} food`)}`;
    }

    const imagePool = type === 'ingredient' || type === 'product' ? INGREDIENT_IMAGES : RECIPE_IMAGES;
    if (!imagePool.length) {
        return `https://source.unsplash.com/800x600/?${encodeURIComponent(`${normalized} food`)}`;
    }

    const index = hashString(`${type}:${normalized}`) % imagePool.length;
    return imagePool[index];
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
    const resolvedUrl = providedUrl || getImageForName(name, type);

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
