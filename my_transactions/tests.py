from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from my_profile.models import Profile
from my_transactions.models import Transactions
from .views import withdraw_fund, withdraw_success
from decimal import Decimal
import sys

# Create your tests here.

class TransactionTestCase(TestCase):
    """
    Testing the failed and completed transactions based on their type.
    Starting balance set to 1000.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, balance=1000.00)
        self.client.login(username='testuser', password='testpassword')

    def test_create_transaction_deposit(self):
        """
        The test should return the balance increased by the deposit amount.
        """
        transaction = Transactions.objects.create(
            user=self.user,
            type='Deposit',
            amount=500.00,
            status='Completed'
        )
        
        self.assertEqual(transaction.type, 'Deposit')
        self.assertEqual(transaction.amount, 500.00)
        self.assertEqual(transaction.status, 'Completed')
        self.profile.balance += transaction.amount
        self.profile.save()

        self.assertEqual(self.profile.balance, 1500.00) 
        
    def test_create_transaction_withdraw(self):
        """
        The test should return the balance decreased by the deposit amount.
        """
        transaction = Transactions.objects.create(
            user=self.user,
            type='Withdraw',
            amount=500.00,
            status='Completed'
        )
        
        self.assertEqual(transaction.type, 'Withdraw')
        self.assertEqual(transaction.amount, 500.00)
        self.assertEqual(transaction.status, 'Completed')
        self.profile.balance -= transaction.amount
        self.profile.save()

        self.assertEqual(self.profile.balance, 500.00) 
        
    def test_create_transaction_received(self):
        """
        The test should return the balance increased by the received amount.
        """
        transaction = Transactions.objects.create(
            user=self.user,
            type='Received',
            amount=500.00,
            status='Completed'
        )
        
        self.assertEqual(transaction.type, 'Received')
        self.assertEqual(transaction.amount, 500.00)
        self.assertEqual(transaction.status, 'Completed')
        self.profile.balance += transaction.amount
        self.profile.save()

        self.assertEqual(self.profile.balance, 1500.00) 
        
    def test_create_transaction_sent(self):
        """
        The test should return the balance decreased by the sent amount.
        """
        transaction = Transactions.objects.create(
            user=self.user,
            type='Sent',
            amount=500.00,
            status='Completed'
        )
        
        self.assertEqual(transaction.type, 'Sent')
        self.assertEqual(transaction.amount, 500.00)
        self.assertEqual(transaction.status, 'Completed')
        self.profile.balance -= transaction.amount
        self.profile.save()

        self.assertEqual(self.profile.balance, 500.00) 
        
    def test_create_withdraw_failed(self):
        transaction = Transactions.objects.create(
            user=self.user,
            type='Withdraw',
            amount=500.00,
            status='Failed'
        )
        
        self.assertEqual(transaction.type, 'Withdraw')
        self.assertEqual(transaction.amount, 500.00)
        self.assertEqual(transaction.status, 'Failed')
        
        self.profile.save()

        self.assertEqual(self.profile.balance, 1000.00) 
    
    def test_create_deposit_failed(self):
        """
        Test should return the unchanged balance since the transaction failed
        """
        transaction = Transactions.objects.create(
            user=self.user,
            type='Deposit',
            amount=500.00,
            status='Failed'
        )
        
        self.assertEqual(transaction.type, 'Deposit')
        self.assertEqual(transaction.amount, 500.00)
        self.assertEqual(transaction.status, 'Failed')
        
        self.profile.save()

        self.assertEqual(self.profile.balance, 1000.00) 
    
    def test_create_send_failed(self):
        """
        Test should return the unchanged balance since the transaction failed
        """
        transaction = Transactions.objects.create(
            user=self.user,
            type='Sent',
            amount=500.00,
            status='Failed'
        )
        
        self.assertEqual(transaction.type, 'Sent')
        self.assertEqual(transaction.amount, 500.00)
        self.assertEqual(transaction.status, 'Failed')
        
        self.profile.save()

        self.assertEqual(self.profile.balance, 1000.00) 
    
    def test_create_receiving_failed(self):
        """
        Test should return the unchanged balance since the transaction failed
        """
        transaction = Transactions.objects.create(
            user=self.user,
            type='Received',
            amount=500.00,
            status='Failed'
        )
        
        self.assertEqual(transaction.type, 'Received')
        self.assertEqual(transaction.amount, 500.00)
        self.assertEqual(transaction.status, 'Failed')
        
        self.profile.save()

        self.assertEqual(self.profile.balance, 1000.00) 