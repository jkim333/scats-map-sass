from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.timezone import datetime, make_aware
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import json
from products.models import Product
from .models import Subscription
from .logics.post_checkout_success import fulfill_order

import stripe

stripe.api_key = settings.STRIPE_API_KEY

FRONTEND_DOMAIN = f'{settings.FRONTEND_DOMAIN}/checkout'

STRIPE_ENDPOINT_SECRET = settings.STRIPE_ENDPOINT_SECRET

if not settings.STRIPE_DEBUG:
    endpoint = stripe.WebhookEndpoint.create(
        url='https://{settings.ALLOWED_HOST}/payments/stripe-webhook/',
        enabled_events=[
            'checkout.session.completed',
        ],
    )


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
                checkout_session = stripe.checkout.Session.create(
                    customer_email=email,
                    success_url=f'{FRONTEND_DOMAIN}/success',
                    cancel_url=f'{FRONTEND_DOMAIN}/cancelled',
                    payment_method_types=['card'],
                    mode='subscription',
                    line_items=[{
                        'price': 'price_1JLMcPCJUgzn1x20Zosa9yT3',
                        'quantity': 1
                    }],
                    metadata={
                        'subscription': True
                    }
                )
            else:
                # custom order consisting of different product items
                orders = request.data.get('orders')
                product_orders = [
                    {
                        'product': Product.objects.get(id=item['product_id']),
                        'quantity': item['quantity']
                    }
                for item in orders]

                checkout_session = stripe.checkout.Session.create(
                    customer_email=email,
                    payment_method_types=[
                        'card',
                    ],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'aud',
                                'product_data': {
                                    'name': item['product'].name,
                                },
                                'unit_amount': item['product'].unit_price,
                            },
                            'quantity': item['quantity'],
                        } for item in product_orders
                    ],
                    metadata={
                        'product_orders': json.dumps(
                            [
                                {
                                    'product_id': item['product'].id,
                                    'product_name': item['product'].name,
                                    'product_unit_price': item['product'].unit_price,
                                    'product_description': item['product'].description,
                                    'quantity': item['quantity']
                                } for item in product_orders
                            ]
                        )
                    },
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


@require_POST
@csrf_exempt
def stripe_webhook(request):
    try:
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)

class CancelSubscriptionView(APIView):
    """
    Cancel subscription.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        try:
            subscription = user.subscription
            stripe_subscription_id = subscription.stripe_subscription_id
        except Subscription.DoesNotExist:
            return Response(
                {'error': "You don't have any subscription to cancel."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Deactivate subscription both on Stripe and the database
        stripe.Subscription.delete(stripe_subscription_id)
        subscription.active = False
        subscription.removed_at = make_aware(datetime.today())
        subscription.user = None
        subscription.save()
        return Response(
            {'message': 'You have successfully cancelled your subscription.'},
            status=status.HTTP_200_OK
        )
