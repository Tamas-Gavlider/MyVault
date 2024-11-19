import logging
import os
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from my_profile.models import Profile
from my_vault import settings


def send_login_email(email):
    """
    Sending email to user upon succesful login.
    """
    try:
        send_mail(
            'Login Alert',
            """
Hello,

You have successfully logged in to your MyVault account.
If you did not perform this login,
please access your account immediately to change your password.

Thank you,

The MyVault Team
            """,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        logger.info(f"Login email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")


@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    """
    Sending the email if the user activates the notification email option
    """
    try:
        profile = Profile.objects.get(user=user)
        if profile.notificationEmail:
            send_login_email(user.email)
    except Profile.DoesNotExist:
        print("Profile not found for user.")


logger = logging.getLogger(__name__)
