import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from Product_details.models import ProductSpecification, ProductPrice, WarehouseInfo, ShopInfo

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_product_specification(db):
    return ProductSpecification.objects.create(
        id=100,
        name="Test Product",
        description="Test Product Description"
    )

@pytest.fixture
def create_product_price(db, create_product_specification):
    return ProductPrice.objects.create(
        specification_id=create_product_specification.id,
        price=500,
        purchase_price=400
    )

def test_get_all_quantity_list_and_price(api_client, create_product_specification):
    response = api_client.get(reverse('get_all_quantity_list_and_price', args=[create_product_specification.id]))
    assert response.status_code == 200
    assert "data" in response.data

def test_insert_purchase_product_quantity(api_client):
    data = {
        "product_id": 101,
        "specification_id": 202,
        "purchase_price": 450,
        "selling_price": 600,
        "warehouse": [{"warehouse_id": 1, "quantity": 100}],
        "shop": [{"shop_id": 2, "quantity": 50}]
    }
    response = api_client.post(reverse('insert_purchase_product_quantity'), data, format='json')
    assert response.status_code in [200, 201]

def test_subtract_purchase_product_quantity(api_client):
    data = {
        "product_id": 101,
        "specification_id": 202,
        "warehouse": [{"warehouse_id": 1, "quantity": 20}],
        "shop": [{"shop_id": 2, "quantity": 10}]
    }
    response = api_client.post(reverse('subtract_purchase_product_quantity'), data, format='json')
    assert response.status_code in [200, 400]

def test_fetch_selling_price(api_client, create_product_price):
    response = api_client.get(reverse('fetch_selling_price', args=[create_product_price.specification_id]))
    assert response.status_code == 200
    assert response.data["selling_price"] == 500
