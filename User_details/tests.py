import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from User_details.models import Profile, UserBalance, GuestUser

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user_profile(db):
    return Profile.objects.create(
        user_id=1,
        first_name="John",
        last_name="Doe",
        email="johndoe@example.com"
    )

@pytest.fixture
def create_user_balance(db):
    return UserBalance.objects.create(
        user_id=1,
        wallet=100.0,
        point=50.0
    )

def test_login_api(api_client):
    data = {"email": "johndoe@example.com", "password": "password123"}
    response = api_client.post(reverse('login_api'), data, format='json')
    assert response.status_code in [200, 400]

def test_request_password_reset_email(api_client):
    data = {"email": "johndoe@example.com"}
    response = api_client.post(reverse('request_password_reset_email'), data, format='json')
    assert response.status_code == 200

def test_password_token_check(api_client):
    response = api_client.get(reverse('password_token_check', args=["uidb64", "token"]))
    assert response.status_code in [200, 401]

def test_set_new_password(api_client):
    data = {"password": "newpassword123"}
    response = api_client.post(reverse('set_new_password'), data, format='json')
    assert response.status_code == 200

def test_profile_api(api_client, create_user_profile):
    response = api_client.get(reverse('profile_api', args=[create_user_profile.user_id]))
    assert response.status_code == 200

def test_create_specific_user_profile(api_client):
    data = {"user_id": 2, "first_name": "Alice", "last_name": "Smith", "email": "alice@example.com"}
    response = api_client.post(reverse('create_specific_user_profile'), data, format='json')
    assert response.status_code == 201

def test_specific_user_profile(api_client, create_user_profile):
    response = api_client.get(reverse('specific_user_profile', args=[create_user_profile.user_id]))
    assert response.status_code == 200

def test_update_user_profile(api_client, create_user_profile):
    data = {"first_name": "UpdatedName"}
    response = api_client.post(reverse('update_user_profile', args=[create_user_profile.user_id]), data, format='json')
    assert response.status_code == 201

def test_insert_guest_user(api_client):
    data = {"ip_address": "192.168.1.1"}
    response = api_client.post(reverse('insert_guest_user'), data, format='json')
    assert response.status_code == 201

def test_user_balance_value(api_client):
    response = api_client.get(reverse('user_balance_value'))
    assert response.status_code == 200

def test_specific_user_balance_value(api_client, create_user_balance):
    response = api_client.get(reverse('specific_user_balance_value', args=[create_user_balance.user_id]))
    assert response.status_code == 200

def test_add_wallet_value(api_client):
    data = {"user_id": 1, "value": 50}
    response = api_client.post(reverse('add_wallet_value'), data, format='json')
    assert response.status_code == 201

def test_subtract_wallet_value(api_client):
    data = {"user_id": 1, "value": 50}
    response = api_client.post(reverse('subtract_wallet_value'), data, format='json')
    assert response.status_code == 201

def test_point_conversion(api_client):
    data = {"user_id": 1}
    response = api_client.post(reverse('point_conversion'), data, format='json')
    assert response.status_code in [200, 400]

def test_add_point(api_client):
    data = {"user_id": 1, "point": 100}
    response = api_client.post(reverse('add_point'), data, format='json')
    assert response.status_code == 201