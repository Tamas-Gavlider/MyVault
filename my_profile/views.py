from django.shortcuts import render, get_object_or_404
from .models import Profile
from django.contrib.auth.decorators import login_required
import secrets

# Create your views here.


def my_profile(request):
    # Check if the profile exists for the current user, create one if not
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if not profile.sending_address:
        profile.sending_address = secrets.token_hex(10)
        profile.save()  
    if not profile.receiving_address:
        profile.receiving_address = secrets.token_hex(10)
        profile.save()  
    
    
    return render(request, 'profile.html', {"profile": profile})