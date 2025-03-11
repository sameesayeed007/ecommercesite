import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from Advertisement.models import Advertisement

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_ad(db):
    return Advertisement.objects.create(
        title="Test Ad",
        description="Test Description",
        priority=1,
        is_active=True
    )

def test_add_ad(api_client):
    data = {"title": "New Ad", "description": "Sample", "priority": 2, "is_active": True}
    response = api_client.post(reverse('add_ad'), data, format='json')
    assert response.status_code == 201
    assert response.data["success"] is True

def test_show_ad(api_client, create_ad):
    response = api_client.get(reverse('show_ad', args=[create_ad.id]))
    assert response.status_code == 200
    assert response.data["data"]["title"] == "Test Ad"

def test_show_all_ads(api_client):
    response = api_client.get(reverse('show_all_ads'))
    assert response.status_code == 200
    assert response.data["success"] is True

def test_admin_ads(api_client):
    response = api_client.get(reverse('admin_ads'))
    assert response.status_code == 200
    assert response.data["success"] is True

def test_change_status(api_client, create_ad):
    initial_status = create_ad.is_active
    response = api_client.post(reverse('change_status', args=[create_ad.id]))
    assert response.status_code == 200
    create_ad.refresh_from_db()
    assert create_ad.is_active != initial_status

def test_update_ad(api_client, create_ad):
    data = {"title": "Updated Ad", "description": "Updated Description"}
    response = api_client.post(reverse('update_ad', args=[create_ad.id]), data, format='json')
    assert response.status_code == 201
    create_ad.refresh_from_db()
    assert create_ad.title == "Updated Ad"

def test_delete_ad(api_client, create_ad):
    response = api_client.post(reverse('delete_ad', args=[create_ad.id]))
    assert response.status_code == 200
    with pytest.raises(Advertisement.DoesNotExist):
        Advertisement.objects.get(id=create_ad.id)


# Create your tests here.
