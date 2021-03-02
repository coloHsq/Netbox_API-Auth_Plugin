from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path(r'key-exchange/', views.KeyExchangeView.as_view(), name='key_exchange'),
    path(r'api-login/', views.ApiLoginView.as_view(), name='api_login')
]
