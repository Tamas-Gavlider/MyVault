from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Profile
from .forms import ProfileUpdateForm, UserUpdateForm
import secrets
from django.conf import settings


# Create your views here.

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
        
    if not profile.private_key:
        profile.generate_private_key()
        raw_key = profile.raw_key 
    
    return render(request, 'profile.html', {"profile": profile, "raw_key":raw_key if created else None})

@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        form2 = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid() and form2.is_valid():
            form.save()       
            form2.save() 
            return redirect('my_profile')  
    else:
        form = ProfileUpdateForm(instance=profile)
        form2 = UserUpdateForm(instance=request.user)
    
    return render(request, 'update_profile.html', {'form': form, 'form2':form2})

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


@login_required
def validate_private_key(request):
    if request.method == 'POST':
        input_key = request.POST.get('private_key')
        profile = Profile.objects.get(user=request.user)
        
        if profile.validate_private_key(input_key):
            return JsonResponse({'status': 'success', 'message': 'Private key is valid.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid private key.'})

    return render(request, 'validate_key.html')