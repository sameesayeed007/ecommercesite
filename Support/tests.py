import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from Support.models import DeliveryArea, DeliveryLocation, Product

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_delivery_area(db):
    return DeliveryArea.objects.create(
        Area_name="Test Area",
        is_active=True
    )

@pytest.fixture
def create_delivery_location(db, create_delivery_area):
    return DeliveryLocation.objects.create(
        area_id=create_delivery_area.id,
        location_name="Test Location",
        is_active=True
    )

@pytest.fixture
def create_product(db):
    return Product.objects.create(
        id=101,
        lowest_spec_id=-1,
        old_price=0.00,
        new_price=0.00
    )

def test_get_specific_location(api_client, create_delivery_area, create_delivery_location):
    response = api_client.get(reverse('get_specific_location', args=[create_delivery_area.Area_name, 123]))
    assert response.status_code == 200
    assert "data" in response.data

def test_get_estimated_value(api_client):
    data = {"orders": [{"specification_id": 1}]}
    response = api_client.post(reverse('get_estimated_value', args=["Test Area", "Test Location"]), data, format='json')
    assert response.status_code in [200, 400]

def test_make_district_active_inactive(api_client, create_delivery_area):
    response = api_client.post(reverse('make_district_active_inactive', args=[create_delivery_area.Area_name, 0]))
    assert response.status_code == 200

def test_make_thanas_active_inactive(api_client, create_delivery_location):
    response = api_client.post(reverse('make_thanas_active_inactive', args=[create_delivery_location.location_name, 0]))
    assert response.status_code == 200

def test_product_change(api_client):
    response = api_client.post(reverse('product_change'))
    assert response.status_code == 200
