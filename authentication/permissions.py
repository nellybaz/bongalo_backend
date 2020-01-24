from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # # Write permissions are only allowed to the owner of the snippet.
        # token = Token.objects.get(user=obj)
        # return token.key == request.data['token']
        return 1 == 1

    # def has_permission(self, request, view):
    #     user = User.objects.get(request.data['username'])
    #     token = Token.objects.get(user=user)
    #
    #     return token.key == request.data['token']
