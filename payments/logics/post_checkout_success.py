from django.contrib.auth import get_user_model
from django.db import transaction
import json
from functools import reduce
from products.models import Product
from payments.models import Order, OrderItem, Subscription
from datetime import datetime
import pytz
from django.conf import settings


def fulfill_order(session):
    """
    Leave a detailed order record.
    """
    
    customer_email = session['customer_details']['email']
    customer = get_user_model().objects.get(email=customer_email)

    subscription = session['metadata'].get('subscription')

    if subscription == 'True':
        # subscription model
        print(session)
        Subscription.objects.create(
            user=customer,
            email=customer.email,
            stripe_customer_id=session['customer'],
            stripe_subscription_id=session['subscription'],
            total_price=session['amount_total'],
            active=True
        )
    else:
        # custom order consisting of different product items
        product_orders = json.loads(session['metadata']['product_orders'])
        total_price = reduce(
            (lambda x, y: x['product_unit_price']*x['quantity']+y['product_unit_price']*y['quantity']),
            product_orders
        )

        with transaction.atomic():
            order = Order.objects.create(
                user=customer,
                stripe_customer_id=session['customer'],
                stripe_payment_intent_id=session['payment_intent'],
                total_price=total_price,
            )

            order_items = [
                OrderItem(
                    order=order,
                    product=Product.objects.get(id=item['product_id']),
                    product_name=item['product_name'],
                    product_description=item['product_description'],
                    product_unit_price=item['product_unit_price'],
                    quantity=item['quantity']
                ) for item in product_orders
            ]

            OrderItem.objects.bulk_create(order_items)

def cancel_subscription(session):
    stripe_subscription_id = session['id']
    subscription = Subscription.objects.get(
        stripe_subscription_id=stripe_subscription_id
    )
    subscription.active = False
    tz = pytz.timezone(settings.TIME_ZONE)
    ended_at = session['ended_at']
    subscription.ended_at = datetime.fromtimestamp(ended_at, tz)
    subscription.user = None
    subscription.save()

    print('cancel_subscription')

def update_subscription(session):
    try:
        # triggered when updating an existing subscription.
        # i.e. requesting to cancel (not immeidate cancellation)
        # and reactivating subscription.
        stripe_subscription_id = session['id']
        subscription = Subscription.objects.get(
            stripe_subscription_id=stripe_subscription_id
        )
        scheduled_to_cancel_at = session['cancel_at']
        cancellation_requested_at = session['canceled_at']

        tz = pytz.timezone(settings.TIME_ZONE)

        if scheduled_to_cancel_at:
            scheduled_to_cancel_at = datetime.fromtimestamp(scheduled_to_cancel_at, tz)

        if cancellation_requested_at:
            cancellation_requested_at = datetime.fromtimestamp(cancellation_requested_at, tz)

        subscription.scheduled_to_cancel_at = scheduled_to_cancel_at
        subscription.cancellation_requested_at = cancellation_requested_at
        subscription.save()
    except Subscription.DoesNotExist:
        # triggered when creating a new subscription.
        # therefore, subscription does not exist in the database yet.
        pass

    print('update_subscription')
