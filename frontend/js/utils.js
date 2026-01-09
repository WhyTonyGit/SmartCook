// Утилиты для работы с данными и форматированием

// Debounce функция
export function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

export function normalizeText(value) {
    if (!value) return '';
    return value
        .trim()
        .toLowerCase()
        .replace(/ё/g, 'е')
        .replace(/\s+/g, ' ');
}

// Форматирование времени
export function formatTime(minutes) {
    if (!minutes) return '—';
    if (minutes < 60) {
        return `${minutes} мин`;
    }
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (mins === 0) {
        return `${hours} ч`;
    }
    return `${hours} ч ${mins} мин`;
}

// Форматирование рейтинга
export function formatRating(rating) {
    if (!rating) return '0.0';
    return rating.toFixed(1);
}

// Форматирование количества отзывов
export function formatReviews(count) {
    if (!count) return '0 отзывов';
    const lastDigit = count % 10;
    const lastTwoDigits = count % 100;
    
    if (lastTwoDigits >= 11 && lastTwoDigits <= 19) {
        return `${count} отзывов`;
    }
    if (lastDigit === 1) {
        return `${count} отзыв`;
    }
    if (lastDigit >= 2 && lastDigit <= 4) {
        return `${count} отзывов`;
    }
    return `${count} отзывов`;
}

// Форматирование порций
export function formatServings(count) {
    if (!count) return '—';
    const lastDigit = count % 10;
    const lastTwoDigits = count % 100;
    
    if (lastTwoDigits >= 11 && lastTwoDigits <= 19) {
        return `${count} порций`;
    }
    if (lastDigit === 1) {
        return `${count} порция`;
    }
    if (lastDigit >= 2 && lastDigit <= 4) {
        return `${count} порции`;
    }
    return `${count} порций`;
}

// Получить статус рецепта (все ингредиенты есть / нужно докупить)
export function getRecipeStatus(recipe) {
    if (recipe.match_percent === null || recipe.match_percent === undefined) {
        return null;
    }
    if (recipe.match_percent >= 1.0) {
        return 'available';
    }
    if (recipe.missing_ingredients && recipe.missing_ingredients.length > 0) {
        return 'missing';
    }
    return 'available';
}

// Получить текст статуса
export function getRecipeStatusText(recipe) {
    const status = getRecipeStatus(recipe);
    if (status === 'available') {
        return 'Все ингредиенты есть';
    }
    if (status === 'missing') {
        const missing = recipe.missing_ingredients || [];
        if (missing.length > 0) {
            const names = missing.slice(0, 2).map(ing => ing.name).join(', ');
            const more = missing.length > 2 ? ` +${missing.length - 2}` : '';
            return `Нужно: ${names}${more}`;
        }
        return 'Нужно докупить';
    }
    return '';
}

// Показать toast уведомление
export function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#EF4444' : type === 'success' ? '#10B981' : '#8B5CF6'};
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// Показать loading состояние
export function showLoading(container) {
    container.innerHTML = `
        <div class="loading">
            <div class="loading-spinner"></div>
            <p style="margin-top: 1rem;">Загрузка...</p>
        </div>
    `;
}

// Показать empty state
export function showEmptyState(container, message, submessage = '', icon = '📭') {
    container.innerHTML = `
        <div class="empty-state">
            <div class="empty-state-icon">${icon}</div>
            <div class="empty-state-text">${message}</div>
            ${submessage ? `<div class="empty-state-subtext">${submessage}</div>` : ''}
        </div>
    `;
}

// Показать ошибку
export function showError(container, message) {
    container.innerHTML = `
        <div class="alert alert-error">
            ${message}
        </div>
    `;
}

// Парсинг query string
export function getQueryParam(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
}

// Установка query параметра
export function setQueryParam(name, value) {
    const url = new URL(window.location);
    url.searchParams.set(name, value);
    window.history.pushState({}, '', url);
}

// Проверка, является ли устройство мобильным
export function isMobile() {
    return window.innerWidth < 768;
}

// Форматирование даты
export function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 1) return 'только что';
    if (minutes < 60) return `${minutes} мин назад`;
    if (hours < 24) return `${hours} ч назад`;
    if (days < 7) return `${days} дн назад`;
    
    return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
    });
}

// Обрезка текста
export function truncate(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

export function sortRecipes(list, sortKey = 'popular') {
    const items = Array.isArray(list) ? [...list] : [];
    const compareNumber = (a, b) => (Number(b) || 0) - (Number(a) || 0);

    switch (sortKey) {
        case 'time':
            return items.sort((a, b) => (Number(a.cooking_time) || 0) - (Number(b.cooking_time) || 0));
        case 'rating':
            return items.sort((a, b) => compareNumber(a.avg_rating, b.avg_rating));
        case 'popular':
            return items.sort((a, b) => compareNumber(a.comments_count, b.comments_count));
        case 'match':
            return items.sort((a, b) => compareNumber(a.match_percent, b.match_percent));
        case 'name':
            return items.sort((a, b) => (a.title || '').localeCompare(b.title || '', 'ru'));
        default:
            return items;
    }
}
