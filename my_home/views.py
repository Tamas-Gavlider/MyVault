from django.shortcuts import render
from .models import FAQ

# Create your views here.

def my_home(request):
    return render(request, 'home.html')

def faq(request):
    """ A view to return the FAQ page"""
    faqs = FAQ.objects.all()

    return render(request, "faq.html", {'faqs': faqs})