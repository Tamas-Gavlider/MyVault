from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class FAQ(models.Model):
    """
    Model representing Frequently Asked Questions (FAQs).

    Attributes:
        question (CharField): The question being asked.
        answer (TextField): The detailed answer to the question.
    """

    class Meta:
        """
        Customizes the display name of the category in the admin panel.
        """
        verbose_name_plural = 'Frequently Asked Questions'

    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question


class UserQuestion(models.Model):
    """
    User questions asked from AI
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, blank=True)
    question_text = models.TextField()
    date_asked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question by {self.user} on {self.date_asked}"
