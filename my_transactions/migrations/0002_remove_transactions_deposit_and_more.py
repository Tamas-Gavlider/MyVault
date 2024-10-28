# Generated by Django 4.2.16 on 2024-10-28 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_transactions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='deposit',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='money_received',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='money_sent',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='withdraw',
        ),
        migrations.AddField(
            model_name='transactions',
            name='type',
            field=models.CharField(choices=[('Withdraw', 'Withdraw'), ('Deposit', 'Deposit'), ('Sent', 'Sent'), ('Received', 'Received')], default=1, max_length=50),
            preserve_default=False,
        ),
    ]