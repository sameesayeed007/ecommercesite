import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from Impression.models import ProductImpression, Subscribers

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_product_impression(db):
    return ProductImpression.objects.create(
        product_id=100,
        Users=[1, 2, 3],
        view_count=10,
        click_count=5,
        cart_count=2,
        sales_count=1,
        non_verified_user=[-1]
    )

def test_get_specific_product_impression(api_client, create_product_impression):
    response = api_client.get(reverse('get_specific_product_impression', args=[create_product_impression.product_id]))
    assert response.status_code == 200
    assert "product_id" in response.data

def test_insert_product_impression(api_client):
    data = {
        "product_id": 101,
        "Users": [],
        "view_count": 5,
        "click_count": 2,
        "cart_count": 1,
        "sales_count": 0,
        "non_verified_user": [-1]
    }
    response = api_client.post(reverse('insert_product_impression'), data, format='json')
    assert response.status_code == 201
    assert "product_id" in response.data

def test_delete_specific_product_impression(api_client, create_product_impression):
    response = api_client.post(reverse('delete_specific_product_impression', args=[create_product_impression.product_id]))
    assert response.status_code == 204

def test_get_impression_user_id(api_client, create_product_impression):
    response = api_client.get(reverse('get_impression_user_id', args=[create_product_impression.product_id]))
    assert response.status_code == 200
    assert "verified_user_data" in response.data

def test_get_click_impression(api_client, create_product_impression):
    response = api_client.get(reverse('get_click_impression', args=[create_product_impression.product_id]))
    assert response.status_code == 200
    assert "click_impression" in response.data

def test_get_view_impression(api_client, create_product_impression):
    response = api_client.get(reverse('get_view_impression', args=[create_product_impression.product_id]))
    assert response.status_code == 200
    assert "view_impression" in response.data

def test_get_cart_impression(api_client, create_product_impression):
    response = api_client.get(reverse('get_cart_impression', args=[create_product_impression.product_id]))
    assert response.status_code == 200
    assert "cart_impression" in response.data

def test_get_sales_impression(api_client, create_product_impression):
    response = api_client.get(reverse('get_sales_impression', args=[create_product_impression.product_id]))
    assert response.status_code == 200
    assert "sales_impression" in response.data

def test_subscribe(api_client):
    data = {"email": "test@example.com"}
    response = api_client.post(reverse('subscribe'), data, format='json')
    assert response.status_code == 200
    assert response.data["success"] is True
