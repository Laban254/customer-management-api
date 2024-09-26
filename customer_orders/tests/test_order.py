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
    ('', 100, True, status.HTTP_400_BAD_REQUEST),  
    ('Test Item', None, True, status.HTTP_400_BAD_REQUEST),  
    ('Test Item', 100, False, status.HTTP_400_BAD_REQUEST),  
])
@patch('customer_orders.views.send_sms')
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


