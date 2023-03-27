from django.urls import path

from src.services.accounts import user


urlpatterns = [
    path('', user.index)
]