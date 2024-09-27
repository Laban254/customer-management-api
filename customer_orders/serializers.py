from rest_framework import serializers
from .models import Customer, Order
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Customer
import phonenumbers

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
        phone_number_obj = phonenumbers.parse(str(value), None)
        if not phonenumbers.is_valid_number(phone_number_obj):
            raise serializers.ValidationError("The phone number is not valid.")
        
        return value

    def create(self, validated_data):
        """
        Optionally, customize the create logic if needed.
        """
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Order
        fields = ['id', 'item', 'amount', 'time', 'user', 'customer']

class SendSMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    message = serializers.CharField(max_length=160)

    def validate_phone_number(self, value):
        if not value.startswith("+"):
            raise serializers.ValidationError("Phone number must include the country code and start with '+'.")
        return value
