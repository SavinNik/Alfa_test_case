from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from drf_spectacular.utils import extend_schema, OpenApiParameter

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
    permission_classes = [AllowAny]
    queryset = Category.objects.prefetch_related("subcategories").all()
    serializer_class = CategoriesWithSubcategoriesSerializer
    pagination_class = CategoryPagination


class ProductsView(ListAPIView):
    """ Возвращает список продуктов с категорией, подкатегорией и изображениями """
    permission_classes = [AllowAny]
    queryset = Product.objects.select_related("subcategory__category")
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


class CartView(APIView):
    """ Обрабатывает операции с корзиной: добавление, изменение, удаление товаров """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """ Выводит состав корзины с подсчетом количества товаров и суммы стоимости товаров в корзине """
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_product = CartProduct.objects.filter(cart=cart).select_related("product")
        if not cart_product.exists():
            return Response({
                "products": [],
                "total_quantity": 0,
                "total_cost": 0
            })

        products_serializer = CartProductSerializer(cart_product, many=True)
        total_quantity = sum(product.quantity for product in cart_product)
        total_cost = sum(product.product.price for product in cart_product)
        return Response({
            "products": products_serializer.data,
            "total_quantity": total_quantity,
            "total_cost": float(total_cost)
        })

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer", "example": 1},
                    "quantity": {"type": "integer", "example": 3}
                },
                "required": ["product_id", "quantity"]
            }
        },
        responses={
            200: CartProductSerializer,
            404: {"description": "Неверные данные"},
        },
        description="Добавляет продукт в корзину"
    )
    def post(self, request: Request) -> Response:
        """ Добавляет продукт в корзину """
        serializer = AddToCartSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            product_cart = serializer.save()
            response_serializer = CartProductSerializer(product_cart)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request={
          "application/json": {
              "type": "object",
              "properties": {
                  "product_id": {"type": "integer", "example": 1},
                  "quantity": {"type": "integer", "example": 3}
              },
              "required": ["product_id", "quantity"]
          }
        },
        responses={
            200: CartProductSerializer,
            404: {"description": "Продукт не найден в корзине"},
        },
        description="Изменяет количество товара в корзине"
    )
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="product_id",
                type=int,
                location=OpenApiParameter.QUERY,
                description="ID продукта для удаления из корзины",
                required=False
            ),
            OpenApiParameter(
                name="clear",
                type=bool,
                location=OpenApiParameter.QUERY,
                description="Если true — очистить всю корзину",
                required=False
            )
        ],
        responses={
            200: None,
            404: {"description": "Продукт не найден в корзине"},
        },
        description="Удаляет продукт из корзины или очищает корзину полностью"
    )
    def delete(self, request: Request) -> Response:
        """ Удаляет продукт из корзины или очищает корзину полностью"""
        clear_all = request.query_params.get("clear", False)
        product_id = request.query_params.get("product_id")

        cart = Cart.objects.get(user=request.user)

        if clear_all:
            CartProduct.objects.filter(cart=cart).delete()
            return Response(
                {"detail": "Корзина очищена"},
                status=status.HTTP_200_OK
            )

        if product_id is not None:
            try:
                product_id = int(product_id)
            except ValueError:
                return Response(
                    {"error": "product_id должен быть целым числом"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                product_cart = CartProduct.objects.get(cart=cart, product_id=product_id)
                product_cart.delete()
                return Response(
                    {"detail": f"Продукт с ID {product_id} уделен из корзины"},
                    status=status.HTTP_200_OK
                )
            except CartProduct.DoesNotExist:
                return Response(
                    {"error": "Продукт не найден в корзине"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "Не указан product_id или параметр clear"},
                status=status.HTTP_400_BAD_REQUEST
            )


class AuthTokenView(ObtainAuthToken):
    """ Вьюха для получения токена аутентификации """
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})