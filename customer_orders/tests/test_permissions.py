import pytest
from django.contrib.auth.models import User,  AnonymousUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from customer_orders.permission import IsOwner
from customer_orders.models import Customer

@pytest.fixture
def user():
    """Create a user for testing."""
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def other_user():
    """Create another user for testing."""
    return User.objects.create_user(username='otheruser', password='password')

@pytest.fixture
def customer(user):
    """Create a customer instance associated with the user."""
    return Customer.objects.create(user=user)

@pytest.mark.django_db
def test_is_owner_permission(user, other_user, customer):
    """Test the IsOwner permission."""
    factory = APIRequestFactory()
    request = factory.get('/')
    request.user = user  # Set the request user to the owner
    permission = IsOwner()

    assert permission.has_object_permission(request, None, customer) is True

    request.user = other_user  # Set the request user to a different user

    assert permission.has_object_permission(request, None, customer) is False

    request.user = AnonymousUser()  
    assert permission.has_object_permission(request, None, customer) is False