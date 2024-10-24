from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from my_profile.models import Profile  # Adjust based on where Profile model is located

"""
Email notifications
@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    try:
        # Fetch the Profile associated with this user
        profile = Profile.objects.get(user=user)
        email = profile.email  # Or profile.email if email is stored in Profile
        print(f"User {email} logged in!")  # Debugging statement
        send_login_email(email)
    except Profile.DoesNotExist:
        print("Profile not found for user.")
    
def send_login_email(email):
    send_mail(
        'Login Alert',
        'You have logged in successfully.',
        'myvaultbethekey@gmail.com',  # Replace with your actual sender email
        [email],
        fail_silently=False,  # Make sure this is set to False
    )
"""