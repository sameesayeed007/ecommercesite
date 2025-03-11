import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from Managers.models import TransferRequest, Shop, Warehouse

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_transfer_request(db):
    return TransferRequest.objects.create(
        request_setter='sh_1',
        request_getter='wh_2',
        status='Pending'
    )

def test_all_shops_warehouse_lists(api_client):
    response = api_client.get(reverse('all_shops_warehouse_lists'))
    assert response.status_code == 200
    assert "data" in response.data

def test_attend_transfer_product(api_client, create_transfer_request):
    data = {
        "transfer_id": create_transfer_request.id,
        "status": "Approved",
        "approve_data": [{
            "specification_id": 390,
            "approved_qty": 1,
            "approved_user": 1
        }]
    }
    response = api_client.post(reverse('attend_transfer_product'), data, format='json')
    assert response.status_code in [200, 400]

def test_get_user_info(api_client):
    response = api_client.get(reverse('get_user_info', args=[1]))
    assert response.status_code == 200
    assert "houses" in response.data

def test_all_transfer_data_setter(api_client):
    response = api_client.get(reverse('all_transfer_data_setter', args=[0, 1]))
    assert response.status_code == 200
    assert "data" in response.data

def test_get_pending_transfer_data(api_client):
    response = api_client.get(reverse('get_pending_transfer_data', args=[0, 1]))
    assert response.status_code == 200
    assert "data" in response.data

def test_get_particular_transfer_products(api_client, create_transfer_request):
    response = api_client.get(reverse('get_particular_transfer_products', args=[create_transfer_request.id]))
    assert response.status_code == 200
    assert "data" in response.data

def test_all_transfer_data_getter(api_client):
    response = api_client.get(reverse('all_transfer_data_getter', args=[0, 1]))
    assert response.status_code == 200
    assert "data" in response.data
