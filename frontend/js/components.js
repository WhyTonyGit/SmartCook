// Компоненты для рендеринга UI элементов

import { formatTime, formatRating, formatReviews, formatServings, getRecipeStatus, getRecipeStatusText, truncate } from './utils.js';
import { PLACEHOLDER_IMAGE } from './image.js';

const STAR_PATH = 'M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z';

export function renderStars(rating = 0, maxRating = 5, options = {}) {
    const safeRating = Math.max(0, Math.min(Number(rating) || 0, maxRating));
    const size = options.size || 18;
    const className = options.className ? ` ${options.className}` : '';
    const uid = `star-${Math.random().toString(36).slice(2, 9)}`;

    const stars = Array.from({ length: maxRating }, (_, index) => {
        const fill = Math.max(0, Math.min(1, safeRating - index));
        const percent = Math.round(fill * 100);
        const gradientId = `${uid}-${index}`;
        return `
            <svg class="star-icon" viewBox="0 0 24 24" aria-hidden="true">
                <defs>
                    <linearGradient id="${gradientId}" x1="0%" x2="100%">
                        <stop offset="${percent}%" stop-color="var(--star-fill)"></stop>
                        <stop offset="${percent}%" stop-color="var(--star-empty)"></stop>
                    </linearGradient>
                </defs>
                <path d="${STAR_PATH}" fill="url(#${gradientId})"></path>
            </svg>
        `;
    }).join('');

    return `<span class="star-rating${className}" style="--star-size: ${size}px;">${stars}</span>`;
}

// Рендер карточки рецепта
export function renderRecipeCard(recipe, options = {}) {
    const {
        showFavorite = true,
        showStatus = true,
        onClick = null,
        favoriteCallback = null
    } = options;
    
    const status = getRecipeStatus(recipe);
    const statusText = getRecipeStatusText(recipe);
    const imageUrl = recipe.image_url || '';
    
    const favoriteClass = recipe.is_favorite ? 'active' : '';
    const favoriteIcon = recipe.is_favorite 
        ? '<path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>'
        : '<path d="M16.5 3c-1.74 0-3.41.81-4.5 2.09C10.91 3.81 9.24 3 7.5 3 4.42 3 2 5.42 2 8.5c0 3.78 3.4 6.86 8.55 11.54L12 21.35l1.45-1.32C18.6 15.36 22 12.28 22 8.5 22 5.42 19.58 3 16.5 3zm-4.4 15.55l-.1.1-.1-.1C7.14 14.24 4 11.39 4 8.5 4 6.5 5.5 5 7.5 5c1.54 0 3.04.99 3.57 2.36h1.87C13.46 5.99 14.96 5 16.5 5c2 0 3.5 1.5 3.5 3.5 0 2.89-3.14 5.74-7.9 10.05z"/>';
    
    return `
        <div class="recipe-card" ${onClick ? `onclick="${onClick}"` : ''}>
            <div class="recipe-card-image">
                <img src="${PLACEHOLDER_IMAGE}" data-image-url="${imageUrl}" data-image-name="${recipe.title}" data-image-type="recipe" alt="${recipe.title}" loading="lazy">
                ${showFavorite ? `
                    <div class="recipe-card-favorite ${favoriteClass}" ${favoriteCallback ? `onclick="event.stopPropagation(); ${favoriteCallback}"` : ''}>
                        <svg viewBox="0 0 24 24">
                            ${favoriteIcon}
                        </svg>
                    </div>
                ` : ''}
            </div>
            <div class="recipe-card-content">
                <h3 class="recipe-card-title">${recipe.title}</h3>
                ${showStatus && status ? `
                    <div class="recipe-card-status ${status}">
                        ${status === 'available' ? '✓' : '!'} ${statusText}
                    </div>
                ` : ''}
                <div class="recipe-card-meta">
                    <div class="recipe-card-rating">
                        ${renderStars(recipe.avg_rating ?? 0, 5, { size: 16 })}
                        <span class="recipe-card-rating-value">${formatRating(recipe.avg_rating ?? 0)}</span>
                    </div>
                    ${recipe.comments_count ? `
                        <span class="recipe-card-reviews">${formatReviews(recipe.comments_count)}</span>
                    ` : ''}
                    <span>${formatTime(recipe.cooking_time)}</span>
                    <span>${formatServings(5)}</span>
                </div>
                ${recipe.description ? `
                    <div class="recipe-card-description">${truncate(recipe.description, 100)}</div>
                ` : ''}
            </div>
        </div>
    `;
}

// Рендер элемента ингредиента
export function renderIngredientItem(ingredient, options = {}) {
    const {
        showRemove = false,
        onRemove = null,
        showAdd = false,
        onAdd = null
    } = options;
    
    const imageUrl = ingredient.image_url || '';
    
    return `
        <div class="ingredient-item">
            <img src="${PLACEHOLDER_IMAGE}" data-image-url="${imageUrl}" data-image-name="${ingredient.name}" data-image-type="ingredient" alt="${ingredient.name}" class="ingredient-item-image">
            <span class="ingredient-item-name">${ingredient.name}</span>
            ${showRemove && onRemove ? `
                <button class="ingredient-item-remove" onclick="${onRemove}">
                    <svg viewBox="0 0 24 24" width="18" height="18">
                        <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                    </svg>
                </button>
            ` : ''}
            ${showAdd && onAdd ? `
                <button class="ingredient-item-add" onclick="${onAdd}">
                    <svg viewBox="0 0 24 24" width="18" height="18">
                        <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
                    </svg>
                </button>
            ` : ''}
        </div>
    `;
}

// Рендер комментария
export function renderComment(comment, options = {}) {
    const {
        showDelete = false,
        onDelete = null,
        currentUserId = null
    } = options;
    
    const canDelete = showDelete && (currentUserId === comment.consumer_id || options.isAdmin);
    
    return `
        <div class="comment-item">
            <div class="comment-header">
                <div class="comment-author">
                    <div class="comment-avatar">${comment.consumer_username ? comment.consumer_username[0].toUpperCase() : 'U'}</div>
                    <div>
                        <div class="comment-username">${comment.consumer_username || 'Пользователь'}</div>
                        <div class="comment-date">${new Date(comment.created_at).toLocaleDateString('ru-RU')}</div>
                    </div>
                </div>
                ${canDelete && onDelete ? `
                    <button class="comment-delete" onclick="${onDelete}">
                        <svg viewBox="0 0 24 24" width="18" height="18">
                            <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
                        </svg>
                    </button>
                ` : ''}
            </div>
            <div class="comment-text">${comment.text}</div>
        </div>
    `;
}

// Рендер шага приготовления
export function renderStep(step, stepNumber) {
    const imageUrl = step.image_url || '';
    
    return `
        <div class="recipe-step">
            <div class="recipe-step-number">${stepNumber}</div>
            <div class="recipe-step-content">
                <h4 class="recipe-step-title">${step.title}</h4>
                <p class="recipe-step-description">${step.description}</p>
                ${imageUrl ? `
                    <img src="${PLACEHOLDER_IMAGE}" data-image-url="${imageUrl}" alt="${step.title}" class="recipe-step-image">
                ` : ''}
            </div>
        </div>
    `;
}

// Рендер bottom navigation
export function renderBottomNav(currentPage = '') {
    const navItems = [
        { id: 'catalog', icon: 'M4 6h16v2H4zm0 5h16v2H4zm0 5h16v2H4z', label: 'Каталог', href: 'categories.html' },
        { id: 'history', icon: 'M13 3a9 9 0 1 0 8.95 10h-2.02A7 7 0 1 1 13 5c1.61 0 3.09.55 4.26 1.47L15 9h7V2l-2.35 2.35A8.97 8.97 0 0 0 13 3zm-1 5h2v6l5 3-.9 1.48L12 15V8z', label: 'История', href: 'history.html' },
        { id: 'search', icon: 'M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z', label: 'Поиск', href: 'find-recipe.html' },
        { id: 'favorites', icon: 'M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z', label: 'Избранное', href: 'favourites.html' },
        { id: 'profile', icon: 'M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z', label: 'Профиль', href: 'profile.html' }
    ];
    
    return `
        <nav class="bottom-nav">
            ${navItems.map(item => `
                <a href="${item.href}" class="bottom-nav-item ${currentPage === item.id ? 'active' : ''}">
                    <div class="bottom-nav-item-icon">
                        <svg viewBox="0 0 24 24">
                            <path d="${item.icon}"/>
                        </svg>
                    </div>
                    <span>${item.label}</span>
                </a>
            `).join('')}
        </nav>
    `;
}
