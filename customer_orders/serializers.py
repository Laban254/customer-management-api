import logging
from rest_framework import serializers
from .models import Customer, Order
from phonenumber_field.serializerfields import PhoneNumberField
import phonenumbers

logger = logging.getLogger('customer_orders')  

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    phone_number = PhoneNumberField()

    class Meta:
        model = Customer
        fields = ['id', 'name', 'code', 'phone_number', 'user']

    def validate_phone_number(self, value):
        """
        Ensure the phone number starts with a '+' and a valid country code.
        """
        logger.debug('Validating phone number: %s', value)
        phone_number_obj = phonenumbers.parse(str(value), None)
        if not phonenumbers.is_valid_number(phone_number_obj):
            logger.error('Invalid phone number: %s', value)
            raise serializers.ValidationError("The phone number is not valid.")
        
        logger.info('Validated phone number: %s', value)
        return value

    def create(self, validated_data):
        """
        Optionally, customize the create logic if needed.
        """
        customer = super().create(validated_data)
        logger.info('Created new customer: %s', customer)
        return customer

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    customer_id = serializers.PrimaryKeyRelatedField(source='customer', queryset=Customer.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'item', 'amount', 'time', 'user', 'customer_id']

    def create(self, validated_data):
        """
        Optionally, customize the create logic if needed.
        """
        order = super().create(validated_data)
        logger.info('Created new order: %s', order)
        return order

class SendSMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    message = serializers.CharField(max_length=160)

    def validate_phone_number(self, value):
        logger.debug('Validating phone number: %s', value)
        if not value.startswith("+"):
            logger.error('Invalid phone number format: %s', value)
            raise serializers.ValidationError("Phone number must include the country code and start with '+'.")
        
        logger.info('Validated phone number format: %s', value)
        return value