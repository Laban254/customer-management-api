import pytest
from rest_framework import status
from django.urls import reverse
from customer_orders.models import Customer
from customer_orders.views import CustomerListCreateView

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate

@pytest.fixture
def api_request_factory():
    """Fixture to create an API request factory."""
    return APIRequestFactory()

@pytest.fixture
def mock_user(db):
    """Create a mock user for testing."""
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.mark.parametrize("name, code, phone_number, expected_status", [
    ('Test Customer', '123', '+254796111111', status.HTTP_201_CREATED),
    ('', '123', '1234567890', status.HTTP_400_BAD_REQUEST),
    ('Test Customer', '', '1234567890', status.HTTP_400_BAD_REQUEST),
    ('Test Customer', '123', '', status.HTTP_400_BAD_REQUEST),
    ('Test Customer', '123', 'not_a_number', status.HTTP_400_BAD_REQUEST),
])
def test_create_customer_for_authenticated_user(mock_user, api_request_factory, name, code, phone_number, expected_status):
    """Test creating a customer for authenticated users."""
    url = reverse('customer-list-create')
    request = api_request_factory.post(url, {
        'name': name,
        'code': code,
        'phone_number': phone_number,
    })

    force_authenticate(request, user=mock_user)

    response = CustomerListCreateView.as_view()(request) 

    assert response.status_code == expected_status

@pytest.mark.parametrize("authenticated, expected_status", [
    (False, status.HTTP_401_UNAUTHORIZED),
    (True, status.HTTP_200_OK), 
])
def test_access_view_without_authentication(mock_user, api_request_factory, authenticated, expected_status):
    """Test access to a view without authentication."""
    url = reverse('customer-list-create') 
    
    request = api_request_factory.get(url)

    if authenticated:
        force_authenticate(request, user=mock_user)

    response = CustomerListCreateView.as_view()(request) 

    print(expected_status)
    assert response.status_code == expected_status

def test_get_customer_list_authenticated(mock_user, api_request_factory):
    """Test getting the customer list for authenticated users."""
    url = reverse('customer-list-create')
    request = api_request_factory.get(url)
    force_authenticate(request, user=mock_user)

    Customer.objects.create(name='Test Customer', code='123', phone_number='+254796111111', user=mock_user)

    response = CustomerListCreateView.as_view()(request)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0  

def test_get_customer_list_unauthenticated(api_request_factory):
    """Test getting the customer list for unauthenticated users."""
    url = reverse('customer-list-create')
    request = api_request_factory.get(url)

    response = CustomerListCreateView.as_view()(request)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED