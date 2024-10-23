from django.urls import path
from . import views 
from .views import update_profile, location

urlpatterns = [
    path('', views.my_profile, name='my_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/location/', views.location,name="location"),
]