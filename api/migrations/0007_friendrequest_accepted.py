# Generated by Django 5.1.1 on 2025-01-15 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_friendrequest_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
