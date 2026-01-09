import { BASE_URL } from './api.js';

export const PLACEHOLDER_IMAGE = '/static/img/placeholder.svg';

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

    imgEl.dataset.imageUrl = url || '';
    imgEl.onerror = () => {
        if (imgEl.dataset.fallbackApplied === 'true') {
            return;
        }
        imgEl.dataset.fallbackApplied = 'true';
        imgEl.src = PLACEHOLDER_IMAGE;
    };

    imgEl.src = normalizeImageUrl(url);
}

export function applyImageFallbacks(container) {
    if (!container) return;
    container.querySelectorAll('img[data-image-url]').forEach((img) => {
        setImageWithFallback(img, img.dataset.imageUrl);
    });
}
