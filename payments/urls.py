from django.urls import path
from .views import (
    CreateCheckoutSessionView,
    stripe_webhook,
    CancelSubscriptionView,
    ReactivateCancelledSubscriptionView
)

urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view()),
    path('stripe-webhook/', stripe_webhook),
    path('cancel-subscription/', CancelSubscriptionView.as_view()),
    path('reactivate-cancelled-subscription/', ReactivateCancelledSubscriptionView.as_view()),
]