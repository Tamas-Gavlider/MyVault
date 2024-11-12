from django.contrib import admin
from .models import Profile, DeletedProfileLog

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'sending_address', 'receiving_address', 'deletion_requested', 'deletion_request_date', 'suspended')
    list_filter = ('deletion_requested', 'suspended')
    actions = ['approve_deletion_request']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.exclude(user__isnull=True) 

    def approve_deletion_request(self, request, queryset):
        for profile in queryset:
            if profile.deletion_requested:
                # Log the deletion in DeletedProfileLog
                DeletedProfileLog.objects.create(
                    username=profile.user.username,
                    email=profile.user.email
                )
                # Delete the profile and user
                profile.user.delete()
                profile.delete()
    approve_deletion_request.short_description = "Approve and delete selected profiles"

class DeletedProfileLogAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'deletion_date')
    readonly_fields = ('username', 'email', 'deletion_date')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(DeletedProfileLog, DeletedProfileLogAdmin)