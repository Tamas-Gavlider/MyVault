from django import forms
from .models import Profile
from django.contrib.auth.models import User


class ProfileUpdateForm(forms.ModelForm):
    """
    Form to enable/disable email notifications, login location on google maps
    and suspend account"
    """
    class Meta:
        model = Profile
        fields = ['notificationEmail', 'showLocation', 'suspended']
        labels = {
            'notificationEmail': 'Email notifications',
            'showLocation': 'Track location',
            'suspended': 'Suspend'
        }


class UserUpdateForm(forms.ModelForm):
    """
    Update user email - add first and last name of the user
    """
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(
             pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("This email address is already/n"
                                        " in use.")
        return email
