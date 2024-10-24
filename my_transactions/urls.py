from django.urls import path
from . import views 
from .views import my_transactions

urlpatterns = [
    path('', views.my_transactions, name='my_transactions'),
]