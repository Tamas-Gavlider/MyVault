from django.contrib import admin
from .models import Transactions

# Register your models here.

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'status', 'date', 'sending_address', 'receiving_address', 'amount')
    search_fields = ('user__username', 'sending_address', 'receiving_address')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.all()

admin.site.register(Transactions, TransactionsAdmin)