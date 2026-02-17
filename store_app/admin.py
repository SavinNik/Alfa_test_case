from django.contrib import admin

from .models import Category, SubCategory, Product, Cart, CartProduct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Админ-панель для категорий """
    prepopulated_fields = {"slug": ["name"]}
    list_display = ["name", "slug", "image"]
    list_filter = ["name"]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """ Админ-панель для подкатегорий """
    prepopulated_fields = {"slug": ["name"]}
    list_display = ["name", "slug", "image"]
    list_filter = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Админ-панель для продуктов """
    prepopulated_fields = {"slug": ["name"]}
    list_display = ["name", "slug", "price", "image_small", "image_medium", "image_large"]
    list_filter = ["name", "price"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """ Админ-панель для корзин """
    list_display = ["user_id", "created_at"]


@admin.register(CartProduct)
class ProductCartAdmin(admin.ModelAdmin):
    """ Админ-панель для продуктов в корзине """
    list_display = ["product__name", "cart", "quantity"]



