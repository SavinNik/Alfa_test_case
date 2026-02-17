import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_get_categories_with_subcategories(user, category, subcategory, api_client):
    api_client.force_authenticate(user=user)

    url = reverse("categories")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) > 0
    assert response.data["results"][0]["name"] == category.name
    assert len(response.data['results'][0]['subcategories']) > 0