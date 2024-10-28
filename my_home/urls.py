from django.urls import path
from . import views  
from .views import my_home, faq

urlpatterns = [
    path('', views.my_home, name='my_home'),
    path('',views.faq, name='faq')
]