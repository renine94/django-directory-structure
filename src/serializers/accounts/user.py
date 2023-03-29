from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.models.accounts.user import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'is_staff', 'is_active', 'date_joined']
        extra_kwargs = {
            'date_joined': {'read_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError('password 가 같은지 다시 확인부탁드립니다.')
        return data


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
