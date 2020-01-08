from django.http import Http404
from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .serializers import UserSerializer, ProfileSerializer
from authentication.models import UserProfile
from django.contrib.auth.models import User
from authentication.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework import status


# Register Users and create profiles
class RegisterAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = [BasicAuthentication]
    lookup_field = "username"

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_profile = UserProfile.objects.get(user=instance)
            self.perform_destroy(user_profile)
            self.perform_destroy(instance)
            return Response({"responseCode": status.HTTP_200_OK, "successMessage": "success"})
        except Http404:
            pass
        return Response({"responseCode": status.HTTP_204_NO_CONTENT, "errorMessage": "no content"})


class ProfileAPIView(ListAPIView):
    serializer_class = ProfileSerializer
    queryset = UserProfile.objects.all()
