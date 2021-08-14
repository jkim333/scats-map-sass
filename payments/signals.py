from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from djstripe.models import Subscription, Charge


@receiver(post_save, sender=Subscription)
def subscription_handler(sender, **kwargs):
    print('subscription_handler')

    subscription = kwargs['instance']

    customer = subscription.customer
    email = customer.email
    user = get_user_model().objects.get(email=email)
    
    print(subscription.status)
    if subscription.status == 'active':
        user.subscribed = True
        user.subscription_id = subscription.id

    if subscription.status == 'canceled':
        user.subscribed = False
    
    user.save()

@receiver(post_save, sender=Charge)
def charge_handler(sender, **kwargs):
    print('charge_handler')

    charge = kwargs['instance']

    if charge.description == '':
        # the purchase was not a subscription
        pass

