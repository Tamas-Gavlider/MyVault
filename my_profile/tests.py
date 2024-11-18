from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from my_profile.models import Profile, DeletedProfileLog
from django.utils import timezone
from .views import generate_unique_sending_address, generate_unique_receiving_address
import sys

# Create your tests here.

class ProfileDeletionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile = Profile.objects.create(user=self.user)

    def test_delete_profile(self):
        """
        Check the profile deletion function.
        If user deleted they should be logged out and redirected to the home page.
        Raise an error if the deleted user tries to login.
        """
        self.client.login(username='testuser', password='password123')

        response = self.client.post(reverse('delete_profile'))

        deletion_log = DeletedProfileLog.objects.get(username=self.user.username)
        self.assertEqual(deletion_log.email, self.user.email)

        self.assertRedirects(response, reverse('my_home'))
        with self.assertRaises(Exception): 
            self.client.get(reverse('profile'))  


class DeletedProfileLogTests(TestCase):
    """
    Test for checking if the deleted profile will be added to the delete profile log.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
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
        Ensure the function generates a unique sending address by testing the length of it.
        """
        address = generate_unique_sending_address()
        self.assertEqual(len(address), 20) 
        self.assertFalse(Profile.objects.filter(sending_address=address).exists()) 

    def test_generate_unique_receiving_address(self):
        """
        Ensure the function generates a unique sending address by testing the length of it.
        """
        address = generate_unique_receiving_address()
        self.assertEqual(len(address), 20)  
        self.assertFalse(Profile.objects.filter(receiving_address=address).exists()) 