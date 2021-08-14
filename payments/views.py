from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import stripe
from djstripe.models import Subscription
from .serializers import SubscriptionSerializer

if settings.STRIPE_LIVE_MODE:
    stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY
else:
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

FRONTEND_DOMAIN = f'{settings.FRONTEND_DOMAIN}/checkout'


class CreateCheckoutSessionView(APIView):
    """
    Create checkout session in Stripe and return this url as json response.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        email = request.user.email

        try:
            if request.data.get('subscription'):
                # subscription model

                # Do not allow creating more than one subscription
                if request.user.subscribed:
                    return Response(
                        {'error': "You are already on a subscription."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                checkout_session = stripe.checkout.Session.create(
                    customer_email=email,
                    success_url=f'{FRONTEND_DOMAIN}/success',
                    cancel_url=f'{FRONTEND_DOMAIN}/cancelled',
                    payment_method_types=['card'],
                    mode='subscription',
                    line_items=[{
                        'price': settings.STRIPE_SUBSCRIPTION_PRICE_ID,
                        'quantity': 1
                    }],
                )
            else:
                # custom order consisting of different product items
                orders = request.data.get('orders')
                
                if len(orders) == 0: raise Exception('Your order cannot be empty.')

                checkout_session = stripe.checkout.Session.create(
                    customer_email=email,
                    payment_method_types=[
                        'card',
                    ],
                    line_items=[
                        {
                            'price': item['product_id'],
                            'quantity': item['quantity']
                        }
                    for item in orders],
                    mode='payment',
                    success_url=f'{FRONTEND_DOMAIN}/success',
                    cancel_url=f'{FRONTEND_DOMAIN}/cancelled',
                )

            return Response(
                {'checkout_url': checkout_session.url},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class GetSubscriptionInfoView(APIView):
    """
    Get subscription info.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user

        if not user.subscribed:
            return Response(
                {'error': "You do not have any subscription."},
                status=status.HTTP_400_BAD_REQUEST
            )

        subscription_id = user.subscription_id
        subscription = Subscription.objects.get(id=subscription_id)

        serializer = SubscriptionSerializer(subscription)

        return Response(serializer.data)


class CancelSubscriptionView(APIView):
    """
    Cancel subscription.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user

        if not user.subscribed:
            return Response(
                {'error': "You do not have any subscription to cancel."},
                status=status.HTTP_400_BAD_REQUEST
            )

        subscription_id = user.subscription_id

        stripe_subscription = stripe.Subscription.retrieve(subscription_id)

        if stripe_subscription['cancel_at_period_end']:
            return Response(
                {'error': 'Your subscription is already due for cancellation at the end of the current billing period.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        stripe.Subscription.modify(subscription_id, cancel_at_period_end=True)

        return Response(
            {'message': 'Your subscription will be cancelled at the end of the current billing period.'},
            status=status.HTTP_200_OK
        )


class ReactivateCancelledSubscriptionView(APIView):
    """
    Reactivate cancelled subscription.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user

        if not user.subscribed:
            return Response(
                {'error': "You do not have any subscription to reactivate."},
                status=status.HTTP_400_BAD_REQUEST
            )

        subscription_id = user.subscription_id

        stripe_subscription = stripe.Subscription.retrieve(subscription_id)

        if not stripe_subscription['cancel_at_period_end']:
            return Response(
                {'error': "Your subscription is already active."},
                status=status.HTTP_400_BAD_REQUEST
            )

        stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=False
        )

        return Response(
            {'message': 'Your subscription is now successfully reactivated.'},
            status=status.HTTP_200_OK
        )
