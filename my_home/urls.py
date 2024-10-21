from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_home, name='my_home'),
]