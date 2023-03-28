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
router_v1.register('user', user_service.UserAPI, basename='user')
router_v1.register('thesis', thesis_service.ThesisAPI, basename='thesis')

router_v2 = DefaultRouter()
router_v2.register('user', user_service.UserAPI, basename='user')


app_name = 'src'
urlpatterns = [
    path('login/', user_service.MyTokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh'),

    path('logout/', user_service.LogoutView.as_view(), name='logout'),

    path('v1/', include(router_v1.urls)),
    path('v2/', include(router_v2.urls)),
]
