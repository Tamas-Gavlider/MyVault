from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
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

def payment_success(request):
    return render(request, 'transactions/payment_success.html')

def payment_failed(request):
    return render(request, 'payment_failed.html')

def create_checkout_session(request):
    if request.method == "POST":
        try:
            # Parse JSON body to retrieve amount
            data = json.loads(request.body)
            amount = data.get("amount")
            # Create the Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Account Top-Up',
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/transactions/payment_success/'),
                cancel_url=request.build_absolute_uri('/transactions/payment_failed/'),
            )

            # Store the amount in session for later reference
            request.session["payment_amount"] = amount / 100  # Convert to dollars for display
            
            return JsonResponse({'url': checkout_session.url})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
def payment_success(request):
    profile = Profile.objects.get(user=request.user)
    
    amount = request.session.get('payment_amount', None)
    if amount is None:
        Transactions.objects.create(
            user=request.user,
            type='Deposit',
            status='Failed',
            amount=amount,
        )
        profile.save()
        return render(request, 'payment_failed.html', {'error': 'Payment amount is not available.'})

    try:
        amount = Decimal(amount)
        profile.balance += amount
        profile.save()
        
        # Record the transaction
        Transactions.objects.create(
            user=request.user,
            type='Deposit',
            status='Completed',
            amount=amount,
        )

        del request.session['payment_amount']
        return render(request, 'payment_success.html')

    except (ValueError, InvalidOperation):
        return render(request, 'payment_failed.html', {'error': 'Invalid amount.'})

@login_required
def my_transactions(request):
    is_validated = request.session.get('is_validated', False)
    user_transactions = Transactions.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    balance = profile.balance
    context = {
        'is_validated' : is_validated,
        'transactions': user_transactions,
        'profile': profile,
    }
    
    return render(request,'transactions.html', context)

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
                sending_address = f"{sender_profile.user.first_name} {sender_profile.user.last_name}",
                receiving_address=receiving_profile.receiving_address,  
            )

            context = {
                'message': 'Payment sent successfully!',
                'recipient_sending_address': receiving_profile.sending_address,
                'amount': amount
            }

            
            return redirect('my_transactions')

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
                sending_address= f"{sender_profile.user.first_name} {sender_profile.user.last_name}",  
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
    
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    transaction_type = request.GET.get('transaction_type')
    sender_name = request.GET.get('sender_name')

    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)
    if min_amount:
        transactions = transactions.filter(amount__gte=min_amount)
    if max_amount:
        transactions = transactions.filter(amount__lte=max_amount)
    if sender_name:
        transactions = transactions.filter(user= sender_name)
    if transaction_type:
        transactions = transactions.filter(type=transaction_type)

    return render(request, 'transactions_history.html', {'transactions': transactions})
