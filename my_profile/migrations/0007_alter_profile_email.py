# Generated by Django 4.2.16 on 2024-10-24 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_profile', '0006_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
