from django.db import models


class Order(models.Model):
    """
    Order model which records orders ordered by users.
    """
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    stripe_customer_id = models.CharField(max_length=50)
    stripe_payment_intent_id = models.CharField(max_length=50)
    total_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order id: {self.pk}'


class OrderItem(models.Model):
    """
    Detail about individual order item.
    """
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    product_unit_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()


class Subscription(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    stripe_customer_id = models.CharField(max_length=50)
    stripe_subscription_id = models.CharField(max_length=50)
    total_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    cancellation_requested_at = models.DateTimeField(blank=True, null=True)
    scheduled_to_cancel_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return f'Subscription id: {self.pk}'