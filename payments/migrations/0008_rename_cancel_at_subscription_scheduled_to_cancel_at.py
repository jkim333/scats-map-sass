# Generated by Django 3.2.6 on 2021-08-06 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_auto_20210807_0001'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='cancel_at',
            new_name='scheduled_to_cancel_at',
        ),
    ]
