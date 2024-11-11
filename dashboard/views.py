from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from my_transactions.models import Transactions

# Create your views here.

@login_required
def dashboard(request):
    transactions = Transactions.objects.get(user=request.user)
    return render(request,'dashboard.html', {'transactions':transactions})
