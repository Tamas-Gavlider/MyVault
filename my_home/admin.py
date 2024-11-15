from django.contrib import admin
from .models import FAQ, UserQuestion

# Register your models here.


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """
    Customizes the FAQ admin interface.

    This class specifies how the FAQ model
    is displayed in the Django admin interface.
    """
    list_display = ('question', 'answer')


@admin.register(UserQuestion)
class UserQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question_text', 'date_asked')
    list_filter = ('date_asked',)
    search_fields = ('question_text', 'user__username')
    