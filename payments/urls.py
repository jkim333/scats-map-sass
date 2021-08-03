from django.urls import path, include
from .views import CreateCheckoutSessionView

urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view()),
]