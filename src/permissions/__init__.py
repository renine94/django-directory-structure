from django.contrib.auth import get_user_model

from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import IsAuthenticated

from src.models import User


class IsOwnerOnly(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            if isinstance(obj, User):
                return obj == request.user
            return obj.user == request.user
        return False

    def has_permission(self, request, view):
        return super().has_permission(request, view)

