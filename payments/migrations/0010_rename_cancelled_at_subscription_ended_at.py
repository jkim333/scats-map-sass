# Generated by Django 3.2.6 on 2021-08-07 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_subscription_cancellation_requested_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='cancelled_at',
            new_name='ended_at',
        ),
    ]
