from django.urls import path
from . import views
from .views import (update_profile, location, delete_profile,
                    validate_private_key)

urlpatterns = [
    path('', views.my_profile, name='my_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/location/', views.location, name="location"),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('profile/validate/', validate_private_key, name='validate_key'),
]
