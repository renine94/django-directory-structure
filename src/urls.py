from django.urls import path, include
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenRefreshView

from src.services.summary import thesis_service
from src.services.accounts import user_service


router_v1 = DefaultRouter()
router_v1.register('user', user_service.UserAPI, basename='user_v1')
router_v1.register('thesis', thesis_service.ThesisAPI, basename='thesis_v1')

# Test 용도
router_v2 = DefaultRouter()
router_v2.register('user', user_service.UserAPI, basename='user_v2')


app_name = 'src'
urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v2/', include(router_v2.urls)),
]
