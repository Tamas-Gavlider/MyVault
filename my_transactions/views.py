from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from my_profile.models import Profile
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Transactions
from decimal import Decimal
from datetime import datetime
import stripe
import json



# Check if the profile exists for the current user, create one if not

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
                description="Top Up Account",
                metadata={'user_id': request.user.id})
            return render(request, 'payment_form.html', {
                'client_secret': intent.client_secret,
                'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
            })

        except Exception as e:
            Transactions.objects.create(
            user=request.user,
            type='Deposit',  
            status='Failed',  
            amount=amount,
        )
            return render(request, 'payment_failed.html', {'error': str(e)})
    
    return render(request, 'payment_form.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)

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
    
    amount = request.session.get('payment_amount', None)

    if amount is None:
        return render(request, 'payment_failed.html', {'error': 'Payment amount is missing.'})

    amount = Decimal(amount) 

    # Update the user's balance
    profile.balance += amount
    profile.save()

    # Create the transaction record including the amount
    Transactions.objects.create(
        user=request.user,
        type='Deposit',  
        status='Completed',  
        amount=amount, 
    )

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
        'profile': profile,
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
        sending_address = request.POST.get('sending_address')
        amount = request.POST.get('sending_amount')
        
        receiving_profile = Profile.objects.filter(receiving_address=sending_address).first()
        
        if not receiving_profile:
            return render(request, 'send_payment.html', {'error': 'Recipient not found'})
        
        try:
            amount = Decimal(amount)
            if amount <= 0:
                return render(request, 'send_payment.html', {'error': 'Amount must be positive'})

            sender_profile = Profile.objects.get(user=request.user)
            if sender_profile.balance < amount:
                return render(request, 'send_payment.html', {'error': 'Insufficient balance'})

            sender_profile.balance -= amount
            receiving_profile.balance += amount
            sender_profile.save()
            receiving_profile.save()
            # Log the transaction for the sender as "Sent"
            Transactions.objects.create(
                user=request.user,
                type='Sent',
                status='Completed',
                amount=amount,
                sending_address=sender_profile.sending_address,  
                receiving_address=receiving_profile.receiving_address,  
            )

            # Log the transaction for the receiver as "Received"
            Transactions.objects.create(
                user=receiving_profile.user,  
                type='Received',  
                status='Completed',
                amount=amount,
                sending_address=sender_profile.sending_address, 
                receiving_address=receiving_profile.receiving_address,  
            )

            context = {
                'message': 'Payment sent successfully!',
                'recipient_sending_address': receiving_profile.sending_address,
                'amount': amount
            }

            
            return render(request, 'send_payment.html', context)

        except Exception as e:
            # Log the failed transaction for the sender as "Sent"
            Transactions.objects.create(
                user=request.user,
                type='Sent',
                status='Failed',
                amount=amount,
                sending_address=sender_profile.sending_address,  
                receiving_address=receiving_profile.receiving_address,  
            )

            # Log the failed transaction for the receiver as "Received"
            Transactions.objects.create(
                user=receiving_profile.user, 
                type='Received', 
                status='Failed',
                amount=amount,
                sending_address=sender_profile.sending_address,  
                receiving_address=receiving_profile.receiving_address,  
            )
            return render(request, 'send_payment.html', {'error': 'Error processing payment: {}'.format(e)})

    return render(request, 'send_payment.html')


def withdraw_fund(request):
    if request.method == "POST":
        amount = int(request.POST.get("amount"))  # Amount in cents (e.g., 500 for $5)
        user_stripe_id = request.user.profile.stripe_customer_id  

        try:
            charge = stripe.Charge.create(
                customer=user_stripe_id,
                amount=amount,
                currency="usd",
                description="Withdrawal from MyVault",
            )
            return JsonResponse({"status": "success", "message": "Withdrawal successful."})
        except stripe.error.StripeError as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return render(request, "withdraw.html")

@login_required
def transactions_history(request):
    transactions = Transactions.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transactions_history.html', {'transactions': transactions})
