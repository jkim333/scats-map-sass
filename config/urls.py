from django.contrib import admin
from django.urls import path, include
from payments.views import stripe_webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('payments/', include('payments.urls')),
    path('stripe-webhook/', stripe_webhook),
]