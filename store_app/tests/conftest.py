import pytest
from django.contrib.auth import get_user_model
from store_app.models import Category, SubCategory, Product

from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def user(db):
    """Создаёт тестового пользователя"""
    return User.objects.create_user(
        username='test_user',
        email='test_user@test.ru',
        password='testpass1'
    )


@pytest.fixture
def category(db):
    """Создаёт категорию"""
    return Category.objects.create(
        name='Молочная продукция',
        slug='molochnaya-produkciya',
        image='categories/test.jpg'
    )


@pytest.fixture
def subcategory(db, category):
    """Создаёт подкатегорию, связанную с категорией"""
    return SubCategory.objects.create(
        name='Молоко',
        slug='moloko',
        image='subcategories/test.jpg',
        category=category
    )


@pytest.fixture
def product(db, subcategory):
    """Создаёт продукт, связанный с подкатегорией"""
    return Product.objects.create(
        name='Молоко 2,5%',
        slug='moloko-2-5',
        price=89.99,
        subcategory=subcategory
    )

@pytest.fixture
def api_client():
    """Создаёт экземпляр APIClient для тестов API"""
    return APIClient()