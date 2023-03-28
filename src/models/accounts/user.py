from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.cache import cache

from datetime import timedelta

from src.serializers.summary.thesis import ThesisSerializer


# Create your models here.

class User(AbstractUser):
    token_count = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(3)])
    token_updated_at = models.DateTimeField(default=timezone.now, help_text='토큰 업데이트 시간')

    class Meta:
        ordering = ['-pk']


    def increase_token(self) -> bool:
        """하루 한번 토큰 1 증가 로직"""
        if self.token_count >= 3:
            return False

        diff = timezone.now() - self.token_updated_at
        if diff < timedelta(days=1):
            return False

        self.token_count += 1
        self.token_updated_at = timezone.now()
        self.save()
        return True

    def decrease_token(self, count: int = 1):
        """토큰 감소 기본값 1"""
        if self.token_count - count < 0:
            raise ValueError('토큰 개수가 부족합니다.')

        self.token_count -= count
        self.save()

    def get_cached_thesis_by_url(self, url: str) -> dict or None:
        """캐싱된 URL 데이터 가져오기"""
        if result := cache.get(f'thesis:{url}:user_id:{self.id}'):
            return result

        thesise = self.thesises.filter(url=url)
        if thesise:
            serializer = ThesisSerializer(thesise.first())
            cache.set(f'thesis:{url}:user_id:{self.id}', serializer.data, 60 * 60 * 24)
            return serializer.data

        return None

