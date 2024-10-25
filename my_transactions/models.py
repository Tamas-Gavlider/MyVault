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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    withdraw = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    money_sent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    money_received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=TRANSACTIONS_STATUS, default='Pending')
    date = models.DateTimeField(auto_now_add=True)
    
    
    
    def __str__(self):
        return f'{self.withdraw} - {self.deposit} - {self.money_sent} - {self.money_received}'
        
