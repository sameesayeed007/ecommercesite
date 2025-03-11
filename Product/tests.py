import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from Product.models import ProductCode, Product

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_product_code(db):
    return ProductCode.objects.create(
        product_id=101,
        specification_id=202,
        Barcode="TSC-0000-202",
        SKU="TSC-0000-202"
    )

def test_insert_specific_code_values(api_client):
    data = {
        "product_id": 102,
        "specification_id": 203,
        "manual_SKU": "1234",
        "uid": 456
    }
    response = api_client.post(reverse('insert_specific_code_values'), data, format='json')
    assert response.status_code == 201
    assert "success" in response.data

def test_insert_manual_code_values(api_client, create_product_code):
    data = {"Barcode": "NEW-BARCODE-202", "SKU": "NEW-SKU-202"}
    response = api_client.post(reverse('insert_manual_code_values', args=[create_product_code.specification_id]), data, format='json')
    assert response.status_code == 201

def test_specific_code_delete(api_client, create_product_code):
    response = api_client.post(reverse('specific_code_delete', args=[create_product_code.specification_id]))
    assert response.status_code == 204

def test_pos_products(api_client):
    data = {"API_key": "valid_key"}
    response = api_client.post(reverse('pos_products'), data, format='json')
    assert response.status_code in [200, 403]

def test_edit_images(api_client):
    data = {"oldImage": [], "images": ["base64encodedimage"]}
    response = api_client.post(reverse('edit_images', args=[101]), data, format='json')
    assert response.status_code in [200, 400]

def test_nospecification_products(api_client):
    response = api_client.get(reverse('nospecification_products'))
    assert response.status_code == 200
    assert "data" in response.data

def test_noprice_products(api_client):
    response = api_client.get(reverse('noprice_products'))
    assert response.status_code == 200
    assert "data" in response.data

def test_publish_unpublish_specification(api_client):
    response = api_client.get(reverse('publish_unpublish_specification', args=[202]))
    assert response.status_code == 200

def test_publish_unpublish_product(api_client):
    response = api_client.get(reverse('publish_unpublish_product', args=[101]))
    assert response.status_code == 200
