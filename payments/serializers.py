from rest_framework import serializers
from djstripe.models import Subscription, Price


# class PriceSerializer(serializers.ModelSerializer):



class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'id', 'start_date', 'cancel_At', 'cancel_at_period_end',
            'cancelled_at', 'current_period_start',
            'current_period_end', 'ended_at', 'status'#, 'price'
        ]