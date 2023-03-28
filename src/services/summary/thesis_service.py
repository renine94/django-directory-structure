from django.shortcuts import render
from django.core.cache import cache

from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework_simplejwt.authentication import JWTAuthentication

from core.utils.openai import OpenAI

from src.models.accounts.user import User
from src.models.summary.thesis import Thesis
from src.serializers.summary.thesis import ThesisSerializer
from src.permissions import IsOwnerOnly


class ThesisAPI(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    queryset = Thesis.objects.all()
    serializer_class = ThesisSerializer
    authentication_classes = (JWTAuthentication, )

    def get_permissions(self):
        """삭제는 staff 거나 내가 요청한 게시물만 가능"""
        if self.action == 'destroy':
            permission_classes = [IsOwnerOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """내가 요청한 요약논문만 가져오기"""
        qs = super().get_queryset()
        return qs.filter(user=self.request.user.id)

    def list(self, request, *args, **kwargs):
        """회원목록 리턴"""
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """단일 회원 목록 리턴"""
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """논문 생성 및 기존에 이미 요청했으면 바로 리턴"""
        user: User = request.user
        url: str = request.data['url']

        if result := user.get_cached_thesis_by_url(url):
            return Response(result)

        if user.token_count < 1:
            return Response({'message': '보유 토큰이 부족합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        self.request.data['user'] = user.id
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        request_url = serializer.validated_data.get('url')
        gpt_answer = OpenAI.get_answer(request_url)
        serializer.validated_data['content'] = gpt_answer
        self.request.user.decrease_token()  # 토큰 사용
        super().perform_create(serializer)

    def perform_destroy(self, instance: Thesis):
        """논문요약 삭제시, cache 데이터도 삭제"""
        cache.delete(f'thesis:{instance.url}:user_id:{instance.user_id}')
        super().perform_destroy(instance)
