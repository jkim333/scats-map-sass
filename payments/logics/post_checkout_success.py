from django.contrib.auth import get_user_model
from django.db import transaction
import json
from functools import reduce
from products.models import Product
from payments.models import Order, OrderItem, Subscription


def fulfill_order(session):
    """
    Leave a detailed order record.
    """
    
    customer_email = session['customer_details']['email']
    customer = get_user_model().objects.get(email=customer_email)

    subscription = session['metadata']['subscription']

    if subscription == 'True':
        # subscription model
        Subscription.objects.create(
            user=customer,
            stripe_customer_id=session['customer'],
            stripe_subscription_id=session['subscription'],
            total_price=session['amount_total']
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
