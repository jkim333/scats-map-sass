# Generated by Django 3.2.6 on 2021-08-09 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_subscribed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='credit',
            new_name='scats_credit',
        ),
        migrations.AddField(
            model_name='user',
            name='seasonality_credit',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
