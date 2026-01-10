import { api } from './api.js';

const LEGACY_PENDING_KEYS = ['prefs:pending', 'prefs:guest'];

function normalizePreferenceIds(value) {
    if (!value) {
        return [];
    }
    try {
        const parsed = JSON.parse(value);
        if (!Array.isArray(parsed)) {
            return [];
        }
        return parsed
            .map((id) => Number(id))
            .filter((id) => Number.isFinite(id));
    } catch (error) {
        return [];
    }
}

function getPendingEmailKey() {
    const pendingEmail = localStorage.getItem('pending_registration_email');
    return pendingEmail ? `prefs:${pendingEmail}` : null;
}

export function getPendingPreferencesKey() {
    return getPendingEmailKey() || LEGACY_PENDING_KEYS[0];
}

export function loadPendingPreferences() {
    const keysToCheck = [];
    const emailKey = getPendingEmailKey();
    if (emailKey) {
        keysToCheck.push(emailKey);
    }
    keysToCheck.push(...LEGACY_PENDING_KEYS);

    for (const key of keysToCheck) {
        const stored = localStorage.getItem(key);
        const items = normalizePreferenceIds(stored);
        if (items.length > 0) {
            return { key, items };
        }
    }

    return { key: getPendingPreferencesKey(), items: [] };
}

export function savePendingPreferences(ingredientIds = []) {
    const key = getPendingPreferencesKey();
    localStorage.setItem(key, JSON.stringify(ingredientIds));
    return key;
}

export async function migratePendingPreferences() {
    const { key, items } = loadPendingPreferences();
    if (!items.length) {
        if (key && localStorage.getItem(key)) {
            localStorage.removeItem(key);
        }
        localStorage.removeItem('pending_registration_email');
        return;
    }

    await api.updateForbiddenIngredients(items);
    localStorage.removeItem(key);
    localStorage.removeItem('pending_registration_email');
}
