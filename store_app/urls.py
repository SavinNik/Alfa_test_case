from django.urls import path

from .views import CategoriesView, ProductsView, CartView, AuthTokenView

urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('products/', ProductsView.as_view(), name='products'),
    path('cart/', CartView.as_view(), name='cart'),
    path('auth-token/', AuthTokenView.as_view(), name='auth-token')
]