import pytest
from customer_orders.serializers import CustomerSerializer, SendSMSSerializer
from customer_orders.models import Customer
from phonenumbers import NumberParseException

@pytest.mark.django_db  
def test_customer_serializer_valid_data():
    """Test valid data for CustomerSerializer."""
    valid_data = {
        'name': 'Test Customer',
        'code': '123',
        'phone_number': '+254796111111',
        'user': 'testuser'
    }
    serializer = CustomerSerializer(data=valid_data)
    assert serializer.is_valid() 
    assert serializer.validated_data['phone_number'] == '+254796111111'

@pytest.mark.django_db  
def test_customer_serializer_invalid_phone_number():
    """Test invalid phone number."""
    invalid_data = {
        'name': 'Test Customer',
        'code': '123',
        'phone_number': '1234567890',  # Invalid phone number
        'user': 'testuser'
    }
    serializer = CustomerSerializer(data=invalid_data)
    assert not serializer.is_valid() 
    assert 'phone_number' in serializer.errors

@pytest.mark.django_db  
def test_send_sms_serializer_valid_data():
    """Test valid data for SendSMSSerializer."""
    valid_data = {
        'phone_number': '+254796111111',
        'message': 'Test message'
    }
    serializer = SendSMSSerializer(data=valid_data)
    assert serializer.is_valid()  

@pytest.mark.django_db 
def test_send_sms_serializer_invalid_phone_number():
    """Test invalid phone number in SendSMSSerializer."""
    invalid_data = {
        'phone_number': '254796111111',  # Missing '+'
        'message': 'Test message'
    }
    serializer = SendSMSSerializer(data=invalid_data)
    assert not serializer.is_valid()  
    assert 'phone_number' in serializer.errors