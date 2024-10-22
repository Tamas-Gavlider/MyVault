from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Corrected
    sending_address = models.CharField(max_length=50, blank=True, null=True)
    receiving_address = models.CharField(max_length=50, blank=True, null=True)
    notificationEmail = models.BooleanField(default=True)
    showLocation = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
        