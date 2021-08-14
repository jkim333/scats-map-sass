from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('payments/', include('payments.urls')),
    path('scats/', include('scats.urls')),
    path('users/', include('users.urls')),
    path('stripe/', include('djstripe.urls', namespace='djstripe')),
]