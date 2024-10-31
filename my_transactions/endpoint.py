import json
import stripe
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    event = None

    # Set your Stripe secret key from settings
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        # Verify the webhook signature (this is optional but recommended)
        # stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        event = json.loads(payload)
    except ValueError as e:
        # Invalid payload
        logger.error(f"Invalid payload: {str(e)}")
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        handle_payment_intent_succeeded(payment_intent)
    elif event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']  # contains a stripe.PaymentMethod
        handle_payment_method_attached(payment_method)
    # ... handle other event types
    else:
        logger.warning(f'Unhandled event type {event["type"]}')

    return HttpResponse(status=200)

def handle_payment_intent_succeeded(payment_intent):
    # Implement your logic to handle successful payment intents here
    logger.info(f'PaymentIntent was successful! ID: {payment_intent["id"]}')
    # e.g., update the user's account balance

def handle_payment_method_attached(payment_method):
    # Implement your logic for when a payment method is attached
    logger.info(f'PaymentMethod was attached: {payment_method["id"]}')