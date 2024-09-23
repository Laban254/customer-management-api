from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    """
    Represents a customer in the system.
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Order(models.Model):
    """
    Represents an order placed by a customer.
    """
    item = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order of {self.item} by {self.customer.name}"
