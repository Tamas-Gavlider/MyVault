# Generated by Django 4.2.16 on 2024-11-19 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_transactions', '0009_alter_transactions_receiving_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='transaction_note',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
