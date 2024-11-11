from django.urls import path
from . import views 

urlpatterns = [
    path('', views.my_home, name='my_home'),
    path('faq/',views.faq, name='faq'),
    path('ask/',views.ask, name='ask')
]