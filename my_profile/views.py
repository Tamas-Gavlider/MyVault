from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core.mail import send_mail
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
    
    # Create the unique sending, receiving address and the private key
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
    """
    Form activate/disable email notification and login location
    Form is for changing the email address
    """
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        form2 = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid() and form2.is_valid():
            form.save()       
            form2.save()
            if profile.notificationEmail == True:
                send_mail(
                'Account Changes Alert',
                """
                Hello,

                We wanted to inform you that changes have been made to your MyVault account. 
                If you did not make these changes, please access your account immediately to change your password.

                Thank you,
            
                The MyVault Team
                """,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
            return redirect('my_profile')  
    else:
        form = ProfileUpdateForm(instance=profile)
        form2 = UserUpdateForm(instance=request.user)
    
    return render(request, 'update_profile.html', {'form': form, 'form2':form2})

@login_required
def delete_profile(request):
    if request.method == "POST":
        user_profile = get_object_or_404(Profile, user=request.user)
        user = user_profile.user  
        user_profile.delete() 
        user.delete() 
        print("User and profile deleted successfully.")
        logout(request)  
        return redirect('my_home')
    return render(request, 'delete_profile.html')
    

@login_required
def location(request):
    api_key = settings.GOOGLE_API_KEY
    return render(request, 'location.html', {'google_api_key': api_key})

@login_required
def validate_private_key(request):
    """
    Validate the private key and store validation status in the session.
    """
    if request.method == 'POST':
        input_key = request.POST.get('private_key')
        profile = Profile.objects.get(user=request.user)
        
        if profile.validate_private_key(input_key):
            # Set session variable to indicate validation
            request.session['is_validated'] = True
            profile.suspended = False
            profile.save()
            return redirect('my_transactions')
        else:
            message = 'Invalid private key. Please try again.'
            return render(request, 'validate_key.html', {'message': message, 'status': 'error'})

    return render(request, 'validate_key.html')