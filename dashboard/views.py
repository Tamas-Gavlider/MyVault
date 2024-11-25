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
    is_validated = request.session.get('is_validated', False)
    today = datetime.today()

    # Get the start and end of the current month
    start_of_month = today.replace(day=1)
    end_of_month = today.replace(month=today.month % 12 + 1,
                                 day=1) - timedelta(days=1)

    # Filter transactions for the current month
    transactions = Transactions.objects.filter(
        user=request.user, date__range=(make_aware(
         start_of_month), make_aware(end_of_month)))

    profile = Profile.objects.get(user=request.user)
    balance = profile.balance
    total_inflow = 0
    total_outflow = 0
    total_withdraw = 0
    total_sent = 0
    total_deposit = 0
    total_received = 0
    bar_chart = pygal.Pie(legend_at_bottom=True)
    for transaction in transactions:
        if transaction.status == 'Completed':
            if transaction.type == 'Withdraw':
                total_withdraw += transaction.amount
                total_outflow += transaction.amount
            elif transaction.type == 'Deposit':
                total_deposit += transaction.amount
                total_inflow += transaction.amount
            elif transaction.type == 'Sent':
                total_sent += transaction.amount
                total_outflow += transaction.amount
            elif transaction.type == 'Received':
                total_received += transaction.amount
                total_inflow += transaction.amount
    bar_chart.add(f'Withdraw: {total_withdraw} USD', total_withdraw)
    bar_chart.add(f'Deposit: {total_deposit} USD', total_deposit)
    bar_chart.add(f'Sent: {total_sent} USD', total_sent)
    bar_chart.add(f'Received: {total_received} USD', total_received)
    chart_svg = bar_chart.render().decode('utf-8')
    bar_chart = pygal.HorizontalBar(legend_at_bottom=True)
    current_month = datetime.now().strftime("%B")
    bar_chart.title = f'Account movements for {current_month} (in USD)'
    bar_chart.add(f'Withdraw: {total_withdraw} USD', total_withdraw)
    bar_chart.add(f'Deposit: {total_deposit} USD', total_deposit)
    bar_chart.add(f'Sent: {total_sent} USD', total_sent)
    bar_chart.add(f'Received: {total_received} USD', total_received)
    chart_horizontal = bar_chart.render().decode('utf-8')
    # Thirds chart will reflect the total of inflows and outflows
    bar_chart_2 = pygal.Pie(legend_at_bottom=True)
    bar_chart_2.title = f'Cash flow in USD for {current_month}'
    bar_chart_2.add(f'Money Inflow: {total_inflow}', total_inflow)
    bar_chart_2.add(f'Money Outflow: {total_outflow}', total_outflow)
    chart_total = bar_chart_2.render().decode('utf-8')
    return render(request, 'dashboard.html', {
        'transactions': transactions,
        'profile': profile,
        'chart_svg': chart_svg,
        'chart_horizontal': chart_horizontal,
        'chart_total': chart_total,
        'is_validated': is_validated
    })
