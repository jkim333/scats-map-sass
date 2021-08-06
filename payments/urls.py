from django.urls import path
from .views import (
    CreateCheckoutSessionView,
    stripe_webhook,
    CancelSubscriptionView
)

urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view()),
    path('stripe-webhook/', stripe_webhook),
    path('cancel-subscription/', CancelSubscriptionView.as_view()),
]