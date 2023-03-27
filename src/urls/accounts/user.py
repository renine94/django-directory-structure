from django.urls import path

from src.services.accounts import user


urlpatterns = [
    path('v1/user', user.index),
]
