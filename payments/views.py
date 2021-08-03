from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import stripe

stripe.api_key = settings.STRIPE_API_KEY

FRONTEND_DOMAIN = f'{settings.FRONTEND_DOMAIN}/checkout'

STRIPE_ENDPOINT_SECRET = settings.STRIPE_ENDPOINT_SECRET


class CreateCheckoutSessionView(APIView):
    """
    Create checkout session in Stripe and return this url as json response.
    """
    def post(self, request, format=None):
        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email='kimjihyung3@gmail.com',
                payment_method_types=[
                    'card',
                ],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'aud',
                            'product_data': {
                            'name': 'T-shirt',
                            },
                            'unit_amount': 2000,
                        },
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

def fulfill_order(session):
    # TODO: fill me in
    print("Fulfilling order")
