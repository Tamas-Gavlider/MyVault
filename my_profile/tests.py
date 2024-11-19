from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from my_profile.models import Profile, DeletedProfileLog
from my_profile.forms import ProfileUpdateForm, UserUpdateForm
from unittest.mock import patch
from django.conf import settings
from django.utils import timezone
from .views import (generate_unique_sending_address,
                    generate_unique_receiving_address)
import sys

# Create your tests here.


class ProfileDeletionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='password123')
        self.profile = Profile.objects.create(user=self.user)

    def test_delete_profile(self):
        """
        Check the profile deletion function.
        If user deleted they should be logged out and redirected
        to the home page.
        Raise an error if the deleted user tries to login.
        """
        self.client.login(username='testuser', password='password123')

        response = self.client.post(reverse('delete_profile'))

        deletion_log = DeletedProfileLog.objects.get(
                       username=self.user.username)
        self.assertEqual(deletion_log.email, self.user.email)

        self.assertRedirects(response, reverse('my_home'))
        with self.assertRaises(Exception):
            self.client.get(reverse('profile'))


class DeletedProfileLogTests(TestCase):
    """
    Test for checking if the deleted profile will be added
    to the delete profile log.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='password123')
        self.profile = Profile.objects.create(user=self.user)

    def test_deleted_profile_log_entry(self):
        DeletedProfileLog.objects.create(
            username=self.user.username,
            email='testuser@example.com',
            deletion_date='2024-11-18'
        )

        log_entry = DeletedProfileLog.objects.get(username='testuser')
        self.assertEqual(log_entry.username, 'testuser')
        self.assertEqual(log_entry.email, 'testuser@example.com')


class UniqueAddressTests(TestCase):
    def test_generate_unique_sending_address(self):
        """
        Ensure the function generates a unique sending address
        by testing the length of it.
        """
        address = generate_unique_sending_address()
        self.assertEqual(len(address), 20)
        self.assertFalse(Profile.objects.filter(
                         sending_address=address).exists())

    def test_generate_unique_receiving_address(self):
        """
        Ensure the function generates a unique sending address
        by testing the length of it.
        """
        address = generate_unique_receiving_address()
        self.assertEqual(len(address), 20)
        self.assertFalse(Profile.objects.filter(
                         receiving_address=address).exists())


class UpdateProfileTestCase(TestCase):
    """
    Test for updating the profile and check if the email notification
    will be sent to the user.
    """
    def setUp(self):
        self.user = User.objects.create_user(
             username='testuser', email='testuser@example.com',
             password='password123')
        self.profile = Profile.objects.create(
            user=self.user,
            notificationEmail=True,
            showLocation=False,
            suspended=False
        )
        self.client = Client()
        self.client.login(username='testuser', password='password123')

    @patch('my_profile.views.send_mail')
    def test_successful_profile_update(self, mock_send_mail):
        data = {
            'notificationEmail': 'on',
            'showLocation': 'on',
            'email': 'newemail@example.com'
        }
        response = self.client.post(reverse('update_profile'), data)

        self.assertRedirects(response, reverse('my_profile'))

        self.profile.refresh_from_db()
        self.user.refresh_from_db()

        self.assertTrue(self.profile.notificationEmail)
        self.assertTrue(self.profile.showLocation)
        self.assertEqual(self.user.email, 'newemail@example.com')
        mock_send_mail.assert_called_once_with(
            'Account Changes Alert',
            """
Hello,

We wanted to inform you that changes have been made to your MyVault account.

If you did not make these changes, please access your account immediately
 to change your password.

Thank you,

The MyVault Team
                """,
            settings.DEFAULT_FROM_EMAIL,
            ['newemail@example.com'],
            fail_silently=False
        )

    def test_get_request_prefills_form(self):

        response = self.client.get(reverse('update_profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_profile.html')
        form = response.context['form']
        form2 = response.context['form2']
        self.assertTrue(form.instance.notificationEmail)
        self.assertFalse(form.instance.showLocation)
        self.assertEqual(form2.instance.email, 'testuser@example.com')
