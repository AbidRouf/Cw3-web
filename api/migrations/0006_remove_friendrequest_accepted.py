# Generated by Django 5.1.1 on 2025-01-15 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_friendrequest_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendrequest',
            name='accepted',
        ),
    ]
