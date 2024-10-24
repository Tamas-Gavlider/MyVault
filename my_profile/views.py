from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Profile
from .forms import ProfileUpdateForm
import secrets
from django.conf import settings

# Create your views here.

@login_required
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

@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')  
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'update_profile.html', {'form': form})

@login_required
def location(request):
    api_key = settings.GOOGLE_API_KEY
    return render(request, 'location.html', {'google_api_key': api_key})
