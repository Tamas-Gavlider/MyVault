from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from my_profile.models import Profile
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Transactions
import stripe


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_form(request):
    return render(request, 'payment_form.html', {'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY})

@login_required
def process_payment(request):
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        print("Stripe Token:", token) 
        try:
            charge = stripe.Charge.create(
                amount=5000,  # Amount in cents (e.g., $50.00)
                currency="usd",
                source=token,
                description="Payment for Order #1234",
            )
            return render(request, 'payment_success.html')
        except stripe.error.CardError as e:
            return render(request, 'payment_failed.html')
    return render(request, 'payment_form.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'status': 'invalid signature'}, status=400)

    if event['type'] == 'charge.succeeded':
        # Handle successful charge
        print("Payment was successful!")

    return JsonResponse({'status': 'success'}, status=200)

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

@login_required
def create_charge(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))  
        customer = stripe.Customer.create(
            email=request.user.email,
            source=request.POST.get('stripeToken')
        )
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Charge for {}'.format(request.user.email)
        )
        Charge.objects.create(user=request.user, amount=amount)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
