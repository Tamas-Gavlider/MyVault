from django.contrib import admin
from .models import Profile, DeletedProfileLog

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'sending_address', 'receiving_address', 'suspended')
    list_filter = ('user','suspended')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.exclude(user__isnull=True) 


class DeletedProfileLogAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'deletion_date')
    readonly_fields = ('username', 'email', 'deletion_date')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(DeletedProfileLog, DeletedProfileLogAdmin)