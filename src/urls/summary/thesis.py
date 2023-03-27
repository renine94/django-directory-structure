from django.urls import path, include

from rest_framework.routers import DefaultRouter

from src.services.summary import thesis


router = DefaultRouter()
router.register('thesis', thesis.ThesisAPI, basename='thesis')

urlpatterns = [
    path('', include(router.urls)),
]
