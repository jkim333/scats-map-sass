from django.urls import path
from .views import (
    CreateCheckoutSessionView,
    stripe_webhook,
    CancelSubscriptionView,
    ReactivateCancelledSubscriptionView,
    GetSubscriptionInfoView
)

urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view()),
    path('stripe-webhook/', stripe_webhook),
    path('cancel-subscription/', CancelSubscriptionView.as_view()),
    path('reactivate-cancelled-subscription/', ReactivateCancelledSubscriptionView.as_view()),
    path('get-subscription-info/', GetSubscriptionInfoView.as_view()),
]