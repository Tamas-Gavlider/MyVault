var stripe = Stripe('pk_test_51QDQ1UJtxNbZKq3VsDXUfk8qOMbjTNKf1iypnwanoWa0TGVlmjL7Iu33EJvCCBIVfcr455R3onLbfBlMGXwdWjwg00Ho0caCwt');
    var elements = stripe.elements();
    var card = elements.create('card', {
        style: {
            base: {
                fontSize: '16px',
                color: '#32325d',
                '::placeholder': {
                    color: '#aab7c4'
                }
            },
            invalid: {
                color: '#fa755a'
            }
        }
    });
    card.mount('#card-element');

    var form = document.getElementById('payment-form');
    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const amount = document.getElementById('amount').value * 100;  // Convert to cents
        // Request the server to create a PaymentIntent with the entered amount
        const response = await fetch("{% url 'create_payment_intent' %}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}"
            },
            body: JSON.stringify({amount: amount})
        });
        const { client_secret } = await response.json();
        const { error, paymentIntent } = await stripe.confirmCardPayment(client_secret, {
            payment_method: {
                card: card,
                billing_details: {
                    email: "{{ request.user.email }}"
                }
            }
        });
        if (error) {
            document.getElementById('card-errors').textContent = error.message;
        } else if (paymentIntent.status === 'succeeded') {
            window.location.href = "{% url 'payment_success' %}";
        }
      });