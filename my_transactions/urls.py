from django.urls import path
from . import views 


urlpatterns = [
    path('', views.my_transactions, name='my_transactions'),
    path('transactions/send_payment/', views.send_payment, name='send_payment'),
    path('transactions/transactions_history/', views.transactions_history, name='transactions_history'),
    path('withdraw/',views.withdraw_fund,name='withdraw_fund'),
    path('create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
]