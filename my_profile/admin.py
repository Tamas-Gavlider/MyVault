from django.contrib import admin
from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance','sending_address', 'receiving_address', )
    search_fields = ('user__username','user__email', 'sending_address', 'receiving_address')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.exclude(user__isnull=True) 
    
admin.site.register(Profile, ProfileAdmin)