from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from src.services.accounts import user


router = DefaultRouter()
router.register('', user.UserAPI, basename='user')


urlpatterns = [
    path('user', include(router.urls)),
    path('login/', user.MyTokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh'),
    path('logout/', user.LogoutView.as_view(), name='logout'),
]
