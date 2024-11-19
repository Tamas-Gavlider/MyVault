from django.contrib import admin, messages
from .models import Transactions

# Register your models here.


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'status', 'date', 'amount',
                    'sending_address', 'receiving_address')
    search_fields = ('user__username', 'sending_address', 'receiving_address')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.all()

    def changelist_view(self, request, extra_context=None):
        """
        Check transactions over 25k and warn the admin
        """
        high_value = self.get_queryset(request).filter(amount__gt=25000.00)
        if high_value.exists():
            messages.warning(
                request,
                f"There are {high_value.count()} transactions over 25,000."
            )
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Transactions, TransactionsAdmin)
