from rest_framework import serializers
from .models import Customer, Order

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Customer
        fields = ['id', 'name', 'code', 'phone_number', 'user']

    def create(self, validated_data):
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Read-only user field

    class Meta:
        model = Order
        fields = ['id', 'item', 'amount', 'time', 'user', 'customer']  # User field included for ownership tracking

class SendSMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    message = serializers.CharField(max_length=160)

    def validate_phone_number(self, value):
        if not value.startswith("+"):
            raise serializers.ValidationError("Phone number must include the country code and start with '+'.")
        return value
