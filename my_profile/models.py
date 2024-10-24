from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    sending_address = models.CharField(max_length=50, blank=True, null=True)
    receiving_address = models.CharField(max_length=50, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notificationEmail = models.BooleanField(default=True)
    showLocation = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.user} - {self.email}'
        