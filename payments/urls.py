from django.urls import path
from .views import (
    CreateCheckoutSessionView,
    CancelSubscriptionView,
    ReactivateCancelledSubscriptionView,
    GetSubscriptionInfoView
)

app_name = 'payments'

urlpatterns = [
    path(
        'create-checkout-session/',
        CreateCheckoutSessionView.as_view(),
        name='create-checkout-session'
    ),
    path(
        'cancel-subscription/',
        CancelSubscriptionView.as_view(),
        name='cancel-subscription'
    ),
    path(
        'reactivate-cancelled-subscription/', ReactivateCancelledSubscriptionView.as_view(),
        name='reactivate-cancelled-subscription'
    ),
    path(
        'get-subscription-info/',
        GetSubscriptionInfoView.as_view(),
        name='get-subscription-info'
    ),
]