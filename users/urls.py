from django.urls import path
from .views import UserDetail

app_name = 'users'

urlpatterns = [
    path(
        '',
        UserDetail.as_view(),
        name='user-detail'
    ),
]