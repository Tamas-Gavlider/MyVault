from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from my_transactions.models import Transactions
from django.utils.timezone import make_aware
from my_profile.models import Profile
from datetime import datetime, timedelta
import pygal 

# Create your views here.

@login_required
def dashboard(request):
    """
    Visualize the user monthly inflow/outflow on pie and bar charts.
    It will reflect the sum for the current month. 
    """
    today = datetime.today()
    
    # Get the start and end of the current month
    start_of_month = today.replace(day=1)
    end_of_month = today.replace(month=today.month % 12 + 1, day=1) - timedelta(days=1)
    
    # Filter transactions for the current month
    transactions = Transactions.objects.filter(user=request.user, date__range=(make_aware(start_of_month), make_aware(end_of_month)))
    
    profile = Profile.objects.get(user=request.user)
    balance = profile.balance
    totalWithdraw = 0
    totalSent = 0
    totalDeposit = 0
    totalReceived = 0
    bar_chart = pygal.Pie()
    for transaction in transactions:
        if transaction.type == 'Withdraw':
            totalWithdraw += transaction.amount
        elif transaction.type == 'Deposit':
            totalDeposit += transaction.amount
        elif transaction.type == 'Sent':
            totalSent += transaction.amount
        elif transaction.type == 'Received':
            totalReceived += transaction.amount
    bar_chart.add('Withdraw', totalWithdraw)
    bar_chart.add('Deposit', totalDeposit)
    bar_chart.add('Sent', totalSent)
    bar_chart.add('Received', totalReceived)
    
    chart_svg = bar_chart.render().decode('utf-8')
    bar_chart = pygal.HorizontalBar()
    current_month = datetime.now().strftime("%B")
    bar_chart.title = f'Account movements for {current_month} (in USD)'
    bar_chart.add('Deposit', totalDeposit)
    bar_chart.add('Withdraw', totalWithdraw)
    bar_chart.add('Sent', totalSent)
    bar_chart.add('Received', totalReceived)
    chart_horizontal = bar_chart.render().decode('utf-8')

    return render(request, 'dashboard.html', {
        'transactions': transactions, 
        'profile': profile, 
        'chart_svg': chart_svg, 
        'chart_horizontal': chart_horizontal,
    })