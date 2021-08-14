from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'company_name', 'scats_credit', 'seasonality_credit',
            'subscribed', 'subscription_id', 'free_until'
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'company_name', 'scats_credit', 'seasonality_credit',
            'subscribed', 'subscription_id', 'free_until'
        ]
        read_only_fields = [
            'id', 'email', 'scats_credit', 'seasonality_credit',
            'subscribed', 'subscription_id', 'free_until'
        ]
