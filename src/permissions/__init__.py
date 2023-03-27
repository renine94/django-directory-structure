from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            return obj.user == request.user
        return False
