import pytest
import json
from service import AuthService

def test_register_endpoint(client):
    response = client.post('/api/auth/register', 
        json={'username': 'testuser', 'email': 'test@example.com', 'password': 'password123'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'access_token' in data

def test_login_endpoint(client, app):
    with app.app_context():
        AuthService.register('testuser', 'test@example.com', None, 'password123')
    
    response = client.post('/api/auth/login',
        json={'emailOrPhone': 'test@example.com', 'password': 'password123'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data

def test_get_ingredients(client):
    response = client.get('/api/ingredients')
    assert response.status_code == 200

def test_get_categories(client):
    response = client.get('/api/categories')
    assert response.status_code == 200

def test_search_recipes(client):
    response = client.get('/api/recipes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_get_recipe(client, app, test_recipe):
    response = client.get(f'/api/recipes/{test_recipe.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Тестовый рецепт'

def test_protected_endpoint_requires_auth(client):
    response = client.get('/api/me')
    assert response.status_code == 401

def test_get_profile_with_token(client, app):
    with app.app_context():
        consumer = AuthService.register('testuser', 'test@example.com', None, 'password123')
        token = AuthService.generate_token(consumer.id)
    
    response = client.get('/api/me', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['email'] == 'test@example.com'

