from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from my_transactions.models import Transactions
from my_profile.models import Profile

# Create your views here.

@login_required
def dashboard(request):
    transactions = Transactions.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    balance = profile.balance
    return render(request,'dashboard.html', {'transactions' : transactions, 'profile': profile})
