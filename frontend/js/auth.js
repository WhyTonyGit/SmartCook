// Утилиты для авторизации и защиты страниц

import { api } from './api.js';

// Проверка авторизации
export async function isAuthenticated() {
    if (!api.getToken()) {
        return false;
    }
    try {
        await api.getProfile();
        return true;
    } catch (error) {
        api.setToken(null);
        return false;
    }
}

// Редирект на логин если не авторизован
export async function requireAuth() {
    const authenticated = await isAuthenticated();
    if (!authenticated) {
        window.location.replace('login.html');
        return false;
    }
    return true;
}

// Проверка и загрузка профиля
export async function checkAuth() {
    const token = api.getToken();
    if (!token) {
        return null;
    }
    
    try {
        const profile = await api.getProfile();
        return profile;
    } catch (error) {
        // Токен невалидный, удаляем его
        api.setToken(null);
        return null;
    }
}

// Обновление навигации в зависимости от авторизации
export async function updateNavigation() {
    const authLinks = document.getElementById('auth-links');
    const userLinks = document.getElementById('user-links');
    
    if (!authLinks || !userLinks) return;
    
    const profile = await checkAuth();
    
    if (profile) {
        authLinks.style.display = 'none';
        userLinks.style.display = 'flex';
        
        // Обновляем имя пользователя если есть элемент
        const usernameEl = document.getElementById('username-nav');
        if (usernameEl) {
            usernameEl.textContent = profile.username;
        }
    } else {
        authLinks.style.display = 'flex';
        userLinks.style.display = 'none';
    }
}

// Инициализация навигации на странице
export function initNavigation() {
    updateNavigation();
    
    // Обновляем при изменении токена (если используется storage event)
    window.addEventListener('storage', (e) => {
        if (e.key === 'access_token') {
            updateNavigation();
        }
    });
}
