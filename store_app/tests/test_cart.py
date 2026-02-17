import pytest
from rest_framework import status
from django.urls import reverse


@pytest.mark.django_db
def test_add_product_to_cart(api_client, user, product):
    api_client.force_authenticate(user=user)
    data = {"product_id": product.id, "quantity": 2}

    url = reverse("cart")
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["quantity"] == "2.00"
    assert response.data["product"] == product.id

@pytest.mark.django_db
def test_update_cart_product_quantity(api_client, user, product):
    api_client.force_authenticate(user=user)
    data = {"product_id": product.id, "quantity": 1}
    url = reverse("cart")
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    update_data = {"product_id": product.id, "quantity": 3}
    response = api_client.put(url, update_data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["quantity"] == "3.00"


@pytest.mark.django_db
def test_remove_product_from_cart(api_client, user, product):
    api_client.force_authenticate(user=user)
    url = reverse('cart')
    data = {'product_id': product.id, 'quantity': 2}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    delete_url = f"{url}?product_id={product.id}"
    response = api_client.delete(delete_url)

    assert response.status_code == status.HTTP_200_OK

