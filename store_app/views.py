from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Category, Product, Cart, CartProduct
from .serializers import (
    CategoriesWithSubcategoriesSerializer,
    ProductSerializer,
    AddToCartSerializer,
    CartProductSerializer
)
from .pagination import CategoryPagination, ProductPagination


class CategoriesView(ListAPIView):
    """ Возвращает список категорий с подкатегориями """
    queryset = Category.objects.prefetch_related("subcategories").all()
    serializer_class = CategoriesWithSubcategoriesSerializer
    pagination_class = CategoryPagination


class ProductsView(ListAPIView):
    """ Возвращает список продуктов с категорией, подкатегорией и изображениями """
    queryset = Product.objects.select_related("subcategory__category")
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


class CartView(APIView):
    """ Обрабатывает операции с корзиной: добавление, изменение, удаление товаров """
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """ Добавляет продукт в корзину """
        serializer = AddToCartSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            product_cart = serializer.save()
            response_serializer = CartProductSerializer(product_cart)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request) -> Response:
        """ Изменяет кол-во продукта в корзине """
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        try:
            cart = Cart.objects.get(user=request.user)
            product_cart = CartProduct.objects.get(cart=cart, product_id=product_id)
        except CartProduct.DoesNotExist:
            return Response(
                {"error": "Продукт не найден в корзине"},
                status=status.HTTP_404_NOT_FOUND
            )

        product_cart.quantity = int(quantity)
        product_cart.save()
        serializer = CartProductSerializer(product_cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request) -> Response:
        """ Удаляет продукт из корзины """
        product_id = request.query_params.get("product_id")
        product_id = int(product_id)

        try:
            cart = Cart.objects.get(user=request.user)
            product_cart = CartProduct.objects.get(cart=cart, product_id=product_id)
            product_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartProduct.DoesNotExist:
            return Response(
                {"error": "Продукт не найден в корзине"},
                status=status.HTTP_404_NOT_FOUND
            )
