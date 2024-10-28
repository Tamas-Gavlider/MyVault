from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
import secrets
import string

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notificationEmail = models.BooleanField(default=True)
    showLocation = models.BooleanField(default=True)
    sending_address = models.CharField(max_length=50, blank=True, null=True)
    receiving_address = models.CharField(max_length=50, blank=True, null=True)
    private_key = models.CharField(max_length=128, blank=True, null=True)
    
    def __str__(self):
        return f'{self.user} - {self.email}'
    
    def generate_private_key(self):
        """
        Generates the unique private key
        """
        characters = string.ascii_letters + string.digits
        raw_key = ''.join(secrets.choice(characters) for i in range(30))
        self.raw_key = raw_key  
        self.private_key = make_password(raw_key)
        self.save()
        
    def validate_private_key(self, input_key):
        """Check if the input key matches the stored hashed private key."""
        return check_password(input_key, self.private_key)
        