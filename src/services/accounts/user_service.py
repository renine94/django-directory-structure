from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_yasg.utils import swagger_auto_schema

from src.models.accounts.user import User
from src.serializers.accounts.user import UserSerializer
from src.serializers.accounts.user import TokenSerializer


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

    @swagger_auto_schema(responses={200: TokenSerializer})
    @action(detail=False, methods=['post'], serializer_class=TokenObtainPairSerializer)
    def login(self, request):
        """Login"""
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            user.increase_token()

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='login-refresh', serializer_class=TokenRefreshSerializer)
    def login_refresh(self, request):
        """로그인 갱신"""
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], authentication_classes=(JWTAuthentication, ), permission_classes=(IsAuthenticated,))
    def logout(self, request):
        """로그아웃 (refresh token 차단)"""
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
