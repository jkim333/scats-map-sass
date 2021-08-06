# Generated by Django 3.2.6 on 2021-08-06 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_alter_subscription_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='email',
            field=models.EmailField(default='kimjihyung3@gmail.com', max_length=254),
            preserve_default=False,
        ),
    ]
