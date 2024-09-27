import pytest
from unittest.mock import patch
from customer_orders.helpers import send_sms

@pytest.mark.parametrize("phone_number, message, expected_status", [
    ('+254796111111', 'Hello, this is a test message.', 'success'),
])
@patch('customer_orders.helpers.sms_service.send')
def test_send_sms_success(mock_send, phone_number, message, expected_status):
    """Test the send_sms function with successful sending."""
    mock_send.return_value = {'status': 'success'}  # Mock response
    response = send_sms(phone_number, message)
    assert response['status'] == expected_status

@patch('customer_orders.helpers.sms_service.send')
def test_send_sms_failure(mock_send):
    """Test the send_sms function when an exception occurs."""
    mock_send.side_effect = Exception("API Error")  # Simulate an exception
    response = send_sms('+254796111111', 'Test message')
    assert response['status'] == 'error'
    assert response['message'] == 'API Error'