# Generated by Django 4.2.16 on 2024-10-28 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_profile', '0009_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='receiving_address',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='sending_address',
        ),
    ]
