from django.shortcuts import render

# Create your views here.

def my_transactions(request):
    return render(request,'transactions.html')