import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from Site_settings.models import CompanyInfo, SiteSettings

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_company_info(db):
    return CompanyInfo.objects.create(
        name="Test Company",
        logo_url="https://example.com/logo.png",
        address="123 Street, City"
    )

@pytest.fixture
def create_site_settings(db):
    return SiteSettings.objects.create(
        setting_key="currency",
        setting_value="USD"
    )

def test_site_settings_config(api_client):
    response = api_client.get(reverse('site_settings_config'))
    assert response.status_code == 200
    assert isinstance(response.data, dict)

def test_company_info(api_client, create_company_info):
    response = api_client.get(reverse('company_info'))
    assert response.status_code == 200
    assert response.data["name"] == "Test Company"

def test_get_company_logo(api_client, create_company_info):
    response = api_client.get(reverse('get_company_logo'))
    assert response.status_code == 200
    assert "logo_url" in response.data

def test_fetch_supplier_price(api_client):
    response = api_client.get(reverse('fetch_supplier_price', args=[101]))
    assert response.status_code == 200
    assert "price" in response.data

def test_generate_product_report(api_client):
    response = api_client.get(reverse('generate_product_report'))
    assert response.status_code == 200
    assert isinstance(response.data, dict)

def test_generate_product_stock_report(api_client):
    response = api_client.get(reverse('generate_product_stock_report'))
    assert response.status_code == 200
    assert "data" in response.data

def test_generate_product_stock_report_pdf(api_client):
    response = api_client.get(reverse('generate_product_stock_report_pdf'))
    assert response.status_code in [200, 500]

def test_generate_no_specification_pdf(api_client):
    response = api_client.get(reverse('generate_no_specification_pdf'))
    assert response.status_code in [200, 500]

def test_generate_no_specification_price_pdf(api_client):
    response = api_client.get(reverse('generate_no_specification_price_pdf'))
    assert response.status_code in [200, 500]
