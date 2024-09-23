from rest_framework import generics
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from .helpers import send_sms

# Customer List and Create View
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve customers associated with the authenticated user."""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Save the new customer instance with the authenticated user."""
        serializer.save(user=self.request.user)

# Order List and Create View
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve orders associated with the authenticated user."""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Save the new order instance and send an SMS notification to the customer."""
        order = serializer.save(user=self.request.user)

        # Send SMS notification
        phone_number = order.customer.phone_number
        message = f"Dear {order.customer.name}, your order for {order.item} has been successfully placed."
        send_sms(phone_number, message)
