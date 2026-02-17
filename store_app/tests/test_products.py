import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_get_products(api_client, product):
    url = reverse("products")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) >= 1
    assert response.data["results"][0]["name"] == product.name
    assert response.data["results"][0]["price"] == str(product.price)