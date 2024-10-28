from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from decimal import Decimal

# Create your models here.


class Transactions(models.Model):
    TRANSACTIONS_STATUS = [
        ('Pending', 'Pending'),
        ('Completed','Completed'),
        ('Failed','Failed'),
        ('Cancelled','Cancelled')
    ]
    
    TRANSACTION_TYPE = [
        ('Withdraw','Withdraw'),
        ('Deposit','Deposit'),
        ('Sent','Sent'),
        ('Received','Received')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=50, choices=TRANSACTION_TYPE)
    status = models.CharField(max_length=50, choices=TRANSACTIONS_STATUS, default='Pending')
    date = models.DateTimeField(auto_now_add=True)
    sending_address = models.CharField(max_length=50, blank=True, null=True)
    receiving_address = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    
    def __str__(self):
        return f'Amount: {self.amount} - {self.type} - {self.status} - {self.date}'
        
