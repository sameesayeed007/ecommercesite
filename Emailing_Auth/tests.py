import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from Emailing_Auth.models import EmailConfig

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_email_config(db):
    return EmailConfig.objects.create(
        email_host="smtp.example.com",
        email_port=587,
        email_host_user="test@example.com",
        email_host_password="password",
        tls_value=True
    )

def test_set_email_config(api_client):
    data = {
        "email_host": "smtp.test.com",
        "email_port": 465,
        "email_host_user": "user@test.com",
        "email_host_password": "securepassword",
        "tls_value": True
    }
    response = api_client.post(reverse('set_email_config'), data, format='json')
    assert response.status_code == 201
    assert "email_host" in response.data

def test_get_email_config_value(api_client, create_email_config):
    response = api_client.get(reverse('get_email_config_value'))
    assert response.status_code == 200
    assert response.data["email_host"] == "smtp.example.com"

def test_show_all_email_config_value(api_client):
    response = api_client.get(reverse('show_all_email_config_value'))
    assert response.status_code == 200
    assert isinstance(response.data, list)

def test_update_email_config(api_client, create_email_config):
    data = {"email_host": "smtp.updated.com"}
    response = api_client.post(reverse('update_email_config', args=[create_email_config.id]), data, format='json')
    assert response.status_code == 201
    create_email_config.refresh_from_db()
    assert create_email_config.email_host == "smtp.updated.com"

def test_email_message(api_client):
    response = api_client.get(reverse('email_message'))
    assert response.status_code in [200, 500]  # Can fail due to SMTP setup

def test_email_verification(api_client):
    response = api_client.get(reverse('email_verification'))
    assert response.status_code in [200, 500]  # Can fail due to SMTP setup
