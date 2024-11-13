from django.shortcuts import render
import google.generativeai as genai
from .models import FAQ, UserQuestion
from django.utils import timezone
import os

# Create your views here.

genai.configure(api_key=os.getenv("GEMINI_API"))

common_questions = {
    "withdraw money": "To withdraw money, go to the transactions page. You need to validate your private key on the profile page to access transactions.",
    "deposit money": "To deposit money, go to the transactions page and follow the Stripe deposit instructions.",
    "send money": "To send money to other users, go to the transactions page, where you can enter the recipient's unique address.",
    "receive money": "To receive money, provide your unique receiving address to the sender, which can be found in your profile.",
    "support" : "To reach out the customer support, please send an email to myvaultbethekey@gmail.com",
    "delete" : "To request account deletion, go to the Profile tab. Once submitted, the request will require approval from the page admin. Please note: Deleting your account will result in the permanent loss of all funds associated with it.",
}

def my_home(request):
    return render(request, 'home.html')

def faq(request):
    """A view to return the FAQ page and provide AI responses with MyVault context."""
    faqs = FAQ.objects.all()
    return render(request, "faq.html", {'faqs': faqs})

def ask(request):
    user_question_text = request.GET.get('question')
    ai_response = ""
    
    if user_question_text:
        # Check if the question matches any predefined responses
        matched_response = next(
            (answer for keyword, answer in common_questions.items() if keyword in user_question_text.lower()), None
        )

        if matched_response:
            ai_response = matched_response
        else:
            # If no match, use generative model with added context
            prompt = (
                "You are MyVault's virtual assistant, here to help users manage their finances. "
                "MyVault allows users to send, receive, deposit, and withdraw money on tesnet. Mainnet is under developemtn. Should go live by Q3 2025."
                "Some actions, like accessing the transactions page, require private key validation. "
                f"User Question: {user_question_text}\nAnswer:"
            )

            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                ai_response = response.text
            except Exception:
                ai_response = "Sorry, I'm unable to answer that question at the moment."

        # Save the user question to the database for admin review
        UserQuestion.objects.create(
            user=request.user if request.user.is_authenticated else None,
            question_text=user_question_text,
            date_asked=timezone.now()
        )
    return render(request, 'ask.html', {'ai_response': ai_response})
