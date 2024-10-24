from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from my_profile.models import Profile
from django.contrib.auth.models import User

from .models import Transactions

# Create your views here.

@login_required
def my_transactions(request):
    user_transactions = Transactions.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    balance = profile.balance
    context = {
        'transactions': user_transactions,
        'balance':balance
    }
    
    return render(request,'transactions.html', context)