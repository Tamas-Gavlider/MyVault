from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from my_profile.models import Profile
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Transactions
from decimal import Decimal, InvalidOperation
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
    """
    Session used for deposit with Stripe.
    """
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
                success_url=request.build_absolute_uri(
                                            '/transactions/payment_success/'),
                cancel_url=request.build_absolute_uri(
                                             '/transactions/payment_failed/'),
            )

            # Store the amount in session for later reference
            # Convert to dollars for display
            request.session["payment_amount"] = amount / 100

            return JsonResponse({'url': checkout_session.url})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


def payment_success(request):
    """
    If payment successful or failed the transaction will be saved to the
    transactions history.
    User will be directed either to payment failed or payment success html
    """
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
        send_mail(
                'Transaction Alert',
                """
Hello,

We wanted to let you know that your recent payment attempt was unsuccessful.

Thank you,

The MyVault Team
                """,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
        return render(request, 'payment_failed.html', {'error':
                      'Payment amount is not available.'})

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
        send_mail(
                'Transaction Alert',
                f"""
Hello,

We're pleased to inform you that your recent top-up of {amount} USD
has been successfully processed.
Your MyVault account balance has been updated.

Thank you,

The MyVault Team
                """,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
        del request.session['payment_amount']
        return render(request, 'payment_success.html')

    except (ValueError, InvalidOperation):
        return render(request, 'payment_failed.html', {'error':
                      'Invalid amount.'})


@login_required
def my_transactions(request):
    """
    User needs to validate the Private Key otherwise the page will be blank
    From profile model the page returns the balance of the user
    """
    is_validated = request.session.get('is_validated', False)
    user_transactions = Transactions.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    balance = profile.balance
    context = {
        'is_validated': is_validated,
        'transactions': user_transactions,
        'profile': profile,
    }

    return render(request, 'transactions.html', context)

# Sending/Receiving payments between users


@login_required
def send_payment(request):
    """
    Send a payment to other users.
    The receiver receiving address will be validated. If the address
    is not valid the sender will be warned.
    Standard validation applied. User must have available balance and
    enter valid amount to make the transaction.
    Transaction will be saved to the transaction history.
    """
    if request.method == 'POST':
        sending_address = request.POST.get('sending_address')
        note = request.POST.get('note')
        amount = request.POST.get('sending_amount')

        receiving_profile = Profile.objects.filter(
                                    receiving_address=sending_address).first()

        if not receiving_profile:
            return render(request, 'send_payment.html', {'error':
                          'Recipient not found'})

        try:
            amount = Decimal(amount)
            if amount <= 0:
                return render(request, 'send_payment.html', {'error':
                              'Amount must be positive'})

            sender_profile = Profile.objects.get(user=request.user)
            if sender_profile.balance < amount:
                return render(request, 'send_payment.html', {'error':
                              'Insufficient balance'})

            sender_profile.balance -= amount
            receiving_profile.balance += amount
            sender_profile.save()
            receiving_profile.save()
            if sender_profile.notificationEmail:
                send_mail(
                 'Transaction Alert',
                 f"""
Hello,

We’re pleased to inform you that your payment of {amount} USD
has been successfully sent to {receiving_profile.receiving_address}.

Thank you,

The MyVault Team
                """,
                 settings.DEFAULT_FROM_EMAIL,
                 [request.user.email],
                 fail_silently=False,
                )
            # Log the transaction for the sender as "Sent"
            Transactions.objects.create(
                user=request.user,
                type='Sent',
                status='Completed',
                transaction_note=note,
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
                transaction_note=note,
                sending_address=f"{sender_profile.user.first_name}/n"
                f" {sender_profile.user.last_name}",
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
                transaction_note=note,
                sending_address=sender_profile.sending_address,
                receiving_address=receiving_profile.receiving_address,
            )

            # Log the failed transaction for the receiver as "Received"
            Transactions.objects.create(
                user=receiving_profile.user,
                type='Received',
                status='Failed',
                amount=amount,
                transaction_note=note,
                sending_address=f"{sender_profile.user.first_name}/n"
                                f" {sender_profile.user.last_name}",
                receiving_address=receiving_profile.receiving_address,
            )
            if sender_profile.notificationEmail:
                send_mail(
                 'Transaction Alert',
                 f"""
Hello,

We wanted to let you know that your recent payment attempt
of {amount} USD to {receiving_profile.receiving_address} was unsuccessful.

Thank you,

The MyVault Team
                """,
                 settings.DEFAULT_FROM_EMAIL,
                 [request.user.email],
                 fail_silently=False,
                )
            return render(request, 'send_payment.html', {'error':
                          'Error processing payment: {}'.format(e)})

    return render(request, 'send_payment.html')


@login_required
def withdraw_success(request):
    return render(request, 'withdraw_success.html')


@login_required
def withdraw(request):
    return render(request, 'withdraw.html')


@login_required
def withdraw_fund(request):
    """
    User enters the amount into the input and click on the withdraw button.
    The amount will be deducted from the balance.
    This function is only for demonstration of the withdraws.
    """
    if request.method == "POST":
        amount = request.POST.get("amount")
        try:
            amount = Decimal(amount)
        except (TypeError, ValueError):
            Transactions.objects.create(
                user=request.user,
                transaction_type='Withdraw',
                status='Failed',
                amount=0,
            )
            return render(request, 'withdraw.html', {'error':
                          'Invalid amount entered.'})

        profile = Profile.objects.get(user=request.user)
        balance = profile.balance
        if balance < amount:
            Transactions.objects.create(
             user=request.user,
             type='Withdraw',
             status='Failed',
             amount=amount,
            )
            return render(request, 'withdraw.html', {'error':
                          'Balance not sufficient'})
        elif amount <= 0:
            Transactions.objects.create(
             user=request.user,
             type='Withdraw',
             status='Failed',
             amount=amount,
            )
            return render(request, 'withdraw.html', {'error':
                          'Minimum withdraw amount is $1'})
        # Deduct amount and save to profile
        profile.balance -= amount
        profile.save()
        if profile.notificationEmail:
            send_mail(
                'Transaction Alert',
                f"""
Hello,

We are pleased to inform you that your withdrawal of {amount} USD
has been successfully processed.

Thank you,

The MyVault Team
                """,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
        # Record the transaction
        Transactions.objects.create(
            user=request.user,
            type='Withdraw',
            status='Completed',
            amount=amount,
        )

        return redirect('withdraw_success')

    return render(request, "transactions.html")


@login_required
def transactions_history(request):
    """
    History of every type of transactions whether completed or failed.
    User can filter by date, amount and transaction type.
    Maximum of 6 transactions will appear on 1 page.
    """
    transactions = Transactions.objects.filter(
                    user=request.user).order_by('-date')

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    transaction_type = request.GET.get('transaction_type')

    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)
    if min_amount:
        transactions = transactions.filter(amount__gte=min_amount)
    if max_amount:
        transactions = transactions.filter(amount__lte=max_amount)
    if transaction_type:
        transactions = transactions.filter(type=transaction_type)

    paginator = Paginator(transactions, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'transactions_history.html', {'page_obj': page_obj})
