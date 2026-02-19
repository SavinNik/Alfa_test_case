from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """ Модель категории продукта """
    name = models.CharField(
        max_length=50,
        null=False,
        unique=True,
        verbose_name="Название категории продукта"
    )
    slug = models.SlugField(null=False)
    image = models.ImageField(
        upload_to="images/",
        null=False,
        verbose_name="Изображение категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.slug}"


class SubCategory(models.Model):
    """ Модель подкатегории продукта """
    name = models.CharField(
        max_length=50,
        null=False,
        unique=True,
        verbose_name="Название подкатегории продукта"
    )
    slug = models.SlugField(null=False)
    image = models.ImageField(
        upload_to="images/",
        null=False,
        verbose_name="Изображение подкатегории"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return f"{self.name} - {self.slug}: {self.category.name}"


class Product(models.Model):
    """ Модель продукта """
    name = models.CharField(
        max_length=100,
        null=False,
        verbose_name="Название продукта"
    )
    slug = models.SlugField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена продукта"
    )
    image_small = models.ImageField(
        upload_to="images/",
        null=True,
        blank=True
    )
    image_medium = models.ImageField(
        upload_to="images/",
        null=True,
        blank=True
    )
    image_large = models.ImageField(
        upload_to="images/",
        null=True,
        blank=True
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="products"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "price"]

    def __str__(self):
        return f"{self.name}: {self.price}"


class Cart(models.Model):
    """ Модель корзины """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина пользователя с ID: {self.user}"


class CartProduct(models.Model):
    """ Модель связи продукта и корзины """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Количество"
    )

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
