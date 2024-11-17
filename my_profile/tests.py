from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from my_profile.models import Profile, DeletedProfileLog
from django.utils import timezone

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
        self.client.login(username='testuser', password='password123')

        
        log_entry = DeletedProfileLog.objects.get(username='testuser')
        self.assertEqual(log_entry.email, self.user.email)
        self.assertEqual(log_entry.username, 'testuser')
        self.assertTrue(log_entry.deletion_date <= timezone.now())