# Generated by Django 5.1.1 on 2025-01-16 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_user_dob'),
    ]

    operations = [
        migrations.DeleteModel(
            name='friendRequests',
        ),
    ]
