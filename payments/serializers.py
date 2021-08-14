from rest_framework import serializers
from djstripe.models import Subscription, Plan, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name']


class PlanSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Plan
        fields = [
            'amount_decimal', 'currency', 'interval',
            'interval_count', 'product'
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()

    class Meta:
        model = Subscription
        fields = [
            'id', 'created', 'cancel_at', 'cancel_at_period_end',
            'canceled_at', 'current_period_start',
            'current_period_end', 'ended_at', 'status', 'plan'
        ]