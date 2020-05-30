from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.method in SAFE_METHODS


class IsOwner(BasePermission):
    """
    allow only profile owners to update ressource
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
