from django.urls import path
from . import views 
from .views import my_transactions, process_payment, stripe_webhook, create_charge, create_payment_intent, payment_success, send_payment, transactions_history

urlpatterns = [
    path('', views.my_transactions, name='my_transactions'),
    path('transactions/payment/', views.process_payment, name='process_payment'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'), 
    path('transactions/create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('send_payment/', views.send_payment, name='send_payment'),
    path('transactions/transactions_history/', views.transactions_history, name='transactions_history')
]