from django.shortcuts import render

# Create your views here.

def my_home(request):
    return render(request, 'home.html')

def faq(request):
    return render(request,'faq.html')