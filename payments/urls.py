from django.urls import path
from .views import CreateCheckoutSessionView, stripe_webhook

urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view()),
    path('stripe-webhook/', stripe_webhook),
]