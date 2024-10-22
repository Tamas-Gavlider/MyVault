from django.shortcuts import render, get_object_or_404
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def my_profile(request):
     profile = get_object_or_404(Profile, user=request.user)
     return render(request, 'profile.html', {
        'profile': profile  
    })