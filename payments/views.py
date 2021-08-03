from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

import stripe

stripe.api_key = settings.STRIPE_API_KEY

FRONTEND_DOMAIN = f'{settings.FRONTEND_DOMAIN}/checkout'

class CreateCheckoutSessionView(APIView):
    """
    Create checkout session in Stripe and return this url as json response.
    """
    def post(self, request, format=None):
        try:
            product = stripe.Product.create(name="Credit Point")

            price = stripe.Price.create(
                        unit_amount=6000, # $50
                        currency="aud",
                        product=product.id
                    )

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=[
                    'card',
                ],
                line_items=[
                    {
                        'price': price.id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=f'{FRONTEND_DOMAIN}/success',
                cancel_url=f'{FRONTEND_DOMAIN}/cancelled',
            )
            return Response(
                {'checkout_url': checkout_session.url},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
