from django.urls import path
from rest_framework import routers
from . import views

urlpatterns = routers.DefaultRouter().urls+[
    path(r'key-exchange/', views.KeyExchangeView.as_view(), name='key_exchange'),
    path(r'api-login/', views.ApiLoginView.as_view(), name='api_login')
]
