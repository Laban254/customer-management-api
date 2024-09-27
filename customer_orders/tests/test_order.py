import pytest
from rest_framework import status
from django.urls import reverse
from customer_orders.models import Customer, Order
from customer_orders.views import OrderListCreateView
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from unittest.mock import patch  # For mocking the send_sms function

@pytest.fixture
def api_request_factory():
    """Fixture to create an API request factory."""
    return APIRequestFactory()

@pytest.fixture
def mock_user(db):
    """Create a mock user for testing."""
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def sample_customer(mock_user, db):
    """Fixture to create a sample customer for testing orders."""
    return Customer.objects.create(name="Test Customer", code="123", phone_number="+254796111111", user=mock_user)

@pytest.mark.parametrize("item, amount, customer, expected_status", [
    ('Test Item', 100, True, status.HTTP_201_CREATED),
    ('', 100, True, status.HTTP_400_BAD_REQUEST),  # Invalid due to missing item
    ('Test Item', None, True, status.HTTP_400_BAD_REQUEST),  
    ('Test Item', 100, False, status.HTTP_400_BAD_REQUEST),  
])
@patch('customer_orders.views.send_sms')  # Mock the send_sms function to prevent real SMS sending
def test_create_order_for_authenticated_user(mock_send_sms, mock_user, api_request_factory, sample_customer, item, amount, customer, expected_status):
    """Test creating an order for authenticated users."""
    url = reverse('order-list-create')
    request_data = {
        'item': item,
        'amount': amount,
        'customer': sample_customer.id if customer else None, 
    }
    request = api_request_factory.post(url, request_data, format='json')

    force_authenticate(request, user=mock_user)
    
    response = OrderListCreateView.as_view()(request)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        assert mock_send_sms.called
    else:
        assert not mock_send_sms.called


@pytest.mark.parametrize("authenticated, expected_status", [
    (False, status.HTTP_401_UNAUTHORIZED),
    (True, status.HTTP_200_OK),
])
def test_access_order_view_without_authentication(mock_user, api_request_factory, authenticated, expected_status):
    """Test access to the order view without authentication."""
    url = reverse('order-list-create') 

    request = api_request_factory.get(url)

    if authenticated:
        force_authenticate(request, user=mock_user)
    
    response = OrderListCreateView.as_view()(request)

    assert response.status_code == expected_status

def test_get_order_list_authenticated(mock_user, sample_customer, api_request_factory):
    """Test getting the order list for authenticated users."""
    url = reverse('order-list-create')
    
    request = api_request_factory.get(url)
    force_authenticate(request, user=mock_user)
    print("Sample Customer:", sample_customer)

    order = Order.objects.create(item='Test Item', amount=100, customer=sample_customer, user=mock_user)

    response = OrderListCreateView.as_view()(request)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0

def test_get_order_list_unauthenticated(api_request_factory):
    """Test getting the order list for unauthenticated users."""
    url = reverse('order-list-create')
    request = api_request_factory.get(url)

    response = OrderListCreateView.as_view()(request)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED