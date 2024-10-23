
from django.dispatch import receiver
from .models import Profile
from .tasks import send_login_email
from django.contrib.auth.signals import user_logged_in


@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    send_login_email(user.email)