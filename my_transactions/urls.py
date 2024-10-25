from django.urls import path
from . import views 
from .views import my_transactions, process_payment, stripe_webhook, create_charge

urlpatterns = [
    path('', views.my_transactions, name='my_transactions'),
    path('transactions/payment/', views.process_payment, name='process_payment'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'), 
]