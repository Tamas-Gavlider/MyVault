import secrets
import string
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notificationEmail = models.BooleanField(default=True)
    showLocation = models.BooleanField(default=True)
    sending_address = models.CharField(max_length=50, blank=True, null=True, unique=True)
    receiving_address = models.CharField(max_length=50, blank=True, null=True, unique=True)
    private_key = models.CharField(max_length=128, blank=True, null=True)
    suspended = models.BooleanField(default=False)
    deletion_requested = models.BooleanField(default=False)
    deletion_request_date = models.DateTimeField(null=True, blank=True)
    last_login = models.CharField(max_length=128, blank=True, null=True)
    
    def __str__(self):
        return f'{self.user} - {self.sending_address} - {self.receiving_address}'
    
    def request_deletion(self):
        """
        Method for user to request deletion
        """
        self.deletion_requested = True
        self.deletion_request_date = timezone.now()
        self.save()
    
    def generate_private_key(self):
        """
        Generates the unique private key using the secrets library
        """
        characters = string.ascii_letters + string.digits
        raw_key = ''.join(secrets.choice(characters) for i in range(30))
        self.raw_key = raw_key  
        self.private_key = make_password(raw_key)
        self.save()
        
    def validate_private_key(self, input_key):
        """Check if the input key matches the stored hashed private key."""
        return check_password(input_key, self.private_key)
    
class DeletedProfileLog(models.Model):
    """
    Keep the deleted users on file
    """
    username = models.CharField(max_length=100)
    email = models.EmailField()
    deletion_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Deleted account: {self.username} on {self.deletion_date}"
    