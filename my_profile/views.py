from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Profile
from .forms import ProfileUpdateForm
import secrets
from django.conf import settings

# Create your views here.

# Generate unique address
def generate_unique_sending_address():
    while True:
        address = secrets.token_hex(10)
        if not Profile.objects.filter(sending_address=address).exists():
            return address
        

def generate_unique_receiving_address():
    while True:
        address = secrets.token_hex(10)
        if not Profile.objects.filter(receiving_address=address).exists():
            return address

@login_required
def my_profile(request):
    # Check if the profile exists for the current user, create one if not
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if not profile.sending_address:
        profile.sending_address = generate_unique_sending_address()
        profile.save()  
    if not profile.receiving_address:
        profile.receiving_address = generate_unique_receiving_address()
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
def delete_profile(request):
    if request.method == "POST":
        user_profile = get_object_or_404(Profile, user=request.user)
        user = user_profile.user  # Get the associated User instance
        user_profile.delete()  # Delete the Profile instance
        user.delete()  # Delete the User instance
        print("User and profile deleted successfully.")
        logout(request)  # Log the user out
        return redirect('my_home')
    return render(request, 'delete_profile.html')
    

@login_required
def location(request):
    api_key = settings.GOOGLE_API_KEY
    return render(request, 'location.html', {'google_api_key': api_key})
