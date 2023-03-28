from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from src.models.accounts.user import User
from src.serializers.accounts.user import UserSerializer


class UserAPI(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()

    def perform_create(self, serializer):
        password = serializer.validated_data.pop('password2')
        serializer.validated_data['password'] = make_password(password)
        super().perform_create(serializer)

    def perform_destroy(self, instance: User) -> None:
        """회원탈퇴 오버라이딩, 실제 DB삭제처리 않고 soft-delete 처리"""
        instance.is_active = False
        instance.save()


class MyTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        """Login"""
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            user.increase_token()
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """로그아웃 (refresh token 차단)"""
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
