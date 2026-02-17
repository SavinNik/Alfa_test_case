from rest_framework import serializers

from .models import Category, SubCategory, Product, CartProduct, Cart



class SubCategorySerializer(serializers.ModelSerializer):
    """ Сериализатор для подкатегорий """
    class Meta:
        model = SubCategory
        fields = ["id", "name", "slug", "image"]


class CategoriesWithSubcategoriesSerializer(serializers.ModelSerializer):
    """ Сериализатор для категорий с подкатегориями """
    subcategories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "image", "subcategories"]


class ProductSerializer(serializers.ModelSerializer):
    """ Сериализатор для продуктов с категориями и подкатегориями и изображениями"""
    category = serializers.CharField(source="subcategory.category.name")
    subcategory = serializers.CharField(source="subcategory.name")
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price", "category", "subcategory", "images"]

    @staticmethod
    def get_images(obj: Product):
        return {
            "small": obj.image_small if obj.image_small else None,
            "medium": obj.image_medium if obj.image_medium else None,
            "large": obj.image_large if obj.image_large else None
        }


class CartProductSerializer(serializers.ModelSerializer):
    """ Сериализатор для продуктов в корзине """
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    class Meta:
        model = CartProduct
        fields = ["id", "product", "quantity", "product_name", "product_price"]


class AddToCartSerializer(serializers.ModelSerializer):
    """ Сериализатор для добавления продуктов в корзину"""
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartProduct
        fields = ["product_id", "quantity"]

    @staticmethod
    def validate_quantity(value):
        if value <= 0:
            raise serializers.ValidationError("Количество должно быть больше 0")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        cart, created = Cart.objects.get_or_create(user=user)
        product_id = validated_data["product_id"]
        quantity = validated_data["quantity"]

        product_cart, created = CartProduct.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={"quantity": quantity}
        )
        if not created:
            product_cart.quantity += quantity
            product_cart.save()
        return product_cart
