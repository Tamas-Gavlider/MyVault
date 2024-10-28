from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

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
    
    
    
    def __str__(self):
        return f'{self.type} - {self.status} - {self.date}'
        
