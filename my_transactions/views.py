from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from my_profile.models import Profile
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Transactions
from decimal import Decimal
import stripe
import json


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_form(request):
    return render(request, 'payment_form.html', {'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY})

@login_required
def process_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount is not None:
            request.session['payment_amount'] = amount
        try:
            
            intent = stripe.PaymentIntent.create(
                amount=amount,           
                currency='usd',
                payment_method_types=['card'],
                description="Payment for Order #1234",
                metadata={'user_id': request.user.id})
            return render(request, 'payment_form.html', {
                'client_secret': intent.client_secret,
                'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
            })

        except Exception as e:
            return render(request, 'payment_failed.html', {'error': str(e)})
    
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
    return JsonResponse({'status': 'success'}, status=200)

@csrf_exempt 
def create_payment_intent(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = data.get('amount') 

            # Create PaymentIntent with the dynamic amount
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=['card']
            )

            return JsonResponse({'client_secret': intent.client_secret})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def payment_success(request):
    profile = Profile.objects.get(user=request.user)
    
    # Retrieve the amount from the session or other relevant source
    amount = request.session.get('payment_amount', None)
    
    # Update the user's balance
    amount = Decimal(amount) 
    profile.balance += amount
    profile.save()
    
    # Clear the amount from session after use
    del request.session['payment_amount']
    
    return render(request, 'payment_success.html')



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

# Sending/Receiving payments between users

@login_required
def send_payment(request):
    if request.method == 'POST':
        # Get values from POST data
        sending_address = request.POST.get('sending_address')
        amount = request.POST.get('sending_amount')
        
        # Find the recipient by receiving address
        receiving_profile = Profile.objects.filter(receiving_address=sending_address).first()
        
        if not receiving_profile:
            return render(request, 'send_payment.html', {'error': 'Recipient not found'})
        
        try:
            amount = Decimal(amount)  # Convert amount to Decimal
            if amount <= 0:
                return render(request, 'send_payment.html', {'error': 'Amount must be positive'})

            # Deduct amount from sender's profile
            sender_profile = Profile.objects.get(user=request.user)
            if sender_profile.balance < amount:
                return render(request, 'send_payment.html', {'error': 'Insufficient balance'})

            sender_profile.balance -= amount
            receiving_profile.balance += amount
            sender_profile.save()
            receiving_profile.save()

            # Redirect or render success message
            return render(request, 'send_payment.html', {'message': 'Payment sent successfully!'})

        except Exception as e:
            return render(request, 'send_payment.html', {'error': 'Error processing payment: {}'.format(e)})

    return render(request, 'send_payment.html')
