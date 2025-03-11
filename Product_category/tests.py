import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from Product_category.models import Category, InventoryReport

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_category(db):
    return Category.objects.create(
        title="Electronics",
        is_active=True
    )

@pytest.fixture
def create_inventory_report(db):
    return InventoryReport.objects.create(
        product_id=101,
        quantity=50,
        transaction_type="Stock-In"
    )

def test_allcategories(api_client):
    response = api_client.get(reverse('allcategories'))
    assert response.status_code == 200
    assert isinstance(response.data, list)

def test_allcategories1(api_client):
    response = api_client.get(reverse('allcategories1'))
    assert response.status_code == 200
    assert isinstance(response.data, list)

def test_categories(api_client):
    response = api_client.get(reverse('categories'))
    assert response.status_code == 200
    assert isinstance(response.data, list)

def test_sub_categories(api_client, create_category):
    data = {"name": create_category.title}
    response = api_client.post(reverse('sub_categories'), data, format='json')
    assert response.status_code == 200
    assert isinstance(response.data, list)

def test_sub_sub_categories(api_client):
    data = {"name": "Mobiles"}
    response = api_client.post(reverse('sub_sub_categories'), data, format='json')
    assert response.status_code == 200
    assert isinstance(response.data, list)

def test_insert_inventory_report(api_client):
    data = {"product_id": 102, "quantity": 20, "transaction_type": "Stock-Out"}
    response = api_client.post(reverse('insert_inventory_report'), data, format='json')
    assert response.status_code == 201

def test_get_inventory_report(api_client, create_inventory_report):
    response = api_client.get(reverse('get_inventory_report', args=[create_inventory_report.product_id]))
    assert response.status_code == 200
    assert "data" in response.data

def test_insert_category1(api_client):
    data = {"category": "Appliances", "sub_category": "Washing Machines", "sub_sub_category": "Front Load"}
    response = api_client.post(reverse('insert_category1'), data, format='json')
    assert response.status_code == 200
