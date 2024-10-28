from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
import logging
from my_profile.models import Profile 
from my_vault import settings

@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    try:
        profile = Profile.objects.get(user=user)
        email = profile.email
        print(f"User {email} logged in!")  # Debugging statement
        print("Sending login email...")  # Debugging statement
        send_login_email(email)
    except Profile.DoesNotExist:
        print("Profile not found for user.")
def send_login_email(email):
    try:
        send_mail(
            'Login Alert',
            'You have logged in successfully.',
            settings.DEFAULT_FROM_EMAIL,  # Use your sender email from settings
            [email],
            fail_silently=False,  # This should be set to False to catch errors
        )
        print(f"Login email sent to {email}")  # Debugging statement
    except Exception as e:
        print(f"Failed to send email: {e}")  # Log the error
        
logger = logging.getLogger(__name__)

def send_login_email(email):
    try:
        send_mail(
            'Login Alert',
            'You have logged in successfully.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        logger.info(f"Login email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")