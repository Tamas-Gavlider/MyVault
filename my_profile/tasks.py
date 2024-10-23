from background_task import background
from django.core.mail import send_mail
from django.conf import settings

@background(schedule=10)
def send_login_email(user_email):
    subject = 'Login Notification'
    message = 'You have successfully logged in to your account.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])