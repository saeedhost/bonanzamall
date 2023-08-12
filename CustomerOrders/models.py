from django.db import models
from django.contrib.auth.models import User
import random

def generate_unique_invoice_number():
    # Generate a random 7-digit number
    return str(random.randint(1000000, 9999999))

class CustomerBilling(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='billings')
    invoice_number = models.CharField(max_length=7, unique=True, default=generate_unique_invoice_number)
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=11)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname

class CustomerBillingItem(models.Model):
    billing = models.ForeignKey(CustomerBilling, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item_name