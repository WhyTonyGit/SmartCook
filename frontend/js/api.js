// API модуль для работы с backend
const API_BASE_URL = 'http://localhost:5000/api';

class API {
    constructor() {
        this.baseURL = API_BASE_URL;
    }

    getToken() {
        return localStorage.getItem('access_token');
    }

    setToken(token) {
        if (token) {
            localStorage.setItem('access_token', token);
        } else {
            localStorage.removeItem('access_token');
        }
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const token = this.getToken();
        
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error?.message || `HTTP error! status: ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Auth
    async register(username, email, phone, password) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, phone, password })
        });
    }

    async login(emailOrPhone, password) {
        const result = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ emailOrPhone, password })
        });
        if (result.access_token) {
            this.setToken(result.access_token);
        }
        return result;
    }

    logout() {
        this.setToken(null);
        window.location.href = '/login.html';
    }

    async getProfile() {
        return this.request('/me');
    }

    async updateProfile(data) {
        return this.request('/me', {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async getForbiddenIngredients() {
        return this.request('/me/forbidden-ingredients');
    }

    async updateForbiddenIngredients(ingredientIds) {
        return this.request('/me/forbidden-ingredients', {
            method: 'PUT',
            body: JSON.stringify({ ingredient_ids: ingredientIds })
        });
    }

    // Recipes
    async searchRecipes(params = {}) {
        const queryParams = new URLSearchParams();
        if (params.q) queryParams.append('q', params.q);
        if (params.ingredients) queryParams.append('ingredients', params.ingredients);
        if (params.minMatch) queryParams.append('minMatch', params.minMatch);
        if (params.maxTime) queryParams.append('maxTime', params.maxTime);
        if (params.difficulty) queryParams.append('difficulty', params.difficulty);
        if (params.categoryId) queryParams.append('categoryId', params.categoryId);
        if (params.sort) queryParams.append('sort', params.sort);
        
        const query = queryParams.toString();
        return this.request(`/recipes?${query}`);
    }

    async getRecipe(recipeId) {
        return this.request(`/recipes/${recipeId}`);
    }

    async getRecommendations() {
        return this.request('/recommendations');
    }

    // Favorites
    async getFavorites() {
        return this.request('/favourites');
    }

    async addFavorite(recipeId) {
        return this.request('/favourites', {
            method: 'POST',
            body: JSON.stringify({ recipe_id: recipeId })
        });
    }

    async removeFavorite(recipeId) {
        return this.request(`/favourites/${recipeId}`, {
            method: 'DELETE'
        });
    }

    // History
    async getHistory() {
        return this.request('/history');
    }

    async addToHistory(recipeId) {
        return this.request('/history', {
            method: 'POST',
            body: JSON.stringify({ recipe_id: recipeId })
        });
    }

    // Ingredients
    async getIngredients(query = '') {
        const params = query ? `?q=${encodeURIComponent(query)}` : '';
        return this.request(`/ingredients${params}`);
    }

    // Categories
    async getCategories() {
        return this.request('/categories');
    }

    // Comments
    async getComments(recipeId) {
        return this.request(`/recipes/${recipeId}/comments`);
    }

    async createComment(recipeId, text) {
        return this.request(`/recipes/${recipeId}/comments`, {
            method: 'POST',
            body: JSON.stringify({ text })
        });
    }

    async deleteComment(commentId) {
        return this.request(`/comments/${commentId}`, {
            method: 'DELETE'
        });
    }

    // Marks
    async upsertMark(recipeId, value) {
        return this.request(`/recipes/${recipeId}/mark`, {
            method: 'POST',
            body: JSON.stringify({ value })
        });
    }

    async getMarks() {
        return this.request('/me/marks');
    }
}

const api = new API();

