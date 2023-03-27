from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.models.summary.thesis import Thesis


class ThesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thesis
        fields = ['id', 'user', 'url', 'content', 'created_at', 'updated_at']
        extra_kwargs = {
            'content': {'read_only': True},
        }

    def validate_url(self, value: str):
        """https://arxiv.org/ 에서 가져오는 논문이어야 한다. validator"""
        if not value.startswith('https://arxiv.org/'):
            raise ValidationError('arxiv.org 에 등재된 논문 PDF URL 링크이어야 합니다.')
        return value
