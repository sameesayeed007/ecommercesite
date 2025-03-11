import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from Cart.models import Order

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_order(db):
    return Order.objects.create(
        is_purchase=True,
        reference_order_id=123,
        mother_site_order_id=456
    )

def test_show_purchase_invoices(api_client):
    response = api_client.get(reverse('show_purchase_invoices'))
    assert response.status_code == 200
    assert "success" in response.data

def test_change_original(api_client, create_order):
    response = api_client.post(reverse('change_original', args=[create_order.id]))
    assert response.status_code == 200
    assert response.data["success"] is True

def test_change_orderdetails_statuses(api_client, create_order):
    data = {
        "order_id": create_order.id,
        "info": [{
            "specification_id": 345,
            "product_status": "None",
            "admin_status": "Pending",
            "mother_admin_status": "Approved",
            "delivery_status": "Pending"
        }]
    }
    response = api_client.post(reverse('change_orderdetails_statuses'), data, format='json')
    assert response.status_code == 200
    assert response.data is not None

def test_find_child_specification_id(api_client):
    response = api_client.get(reverse('find_child_specification_id', args=[345]))
    assert response.status_code == 200
    assert "specification_id" in response.data
