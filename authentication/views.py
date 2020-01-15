from django.http import Http404
from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView
from .serializers import UserSerializer, ProfileSerializer
from authentication.models import UserProfile
from django.contrib.auth.models import User
from .models import UserProfile
from authentication.permissions import IsOwnerOrReadOnly as IsOwnerOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


# Register Users and create profiles at [/api/auth/register/], POST
class RegisterAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            response = super(RegisterAPIView, self).create(request, *args, **kwargs)
            response.data['responseCode'] = 1
            user = User.objects.get(username=response.data['username'])
            token = Token.objects.create(user=user)  # Create token for the new user and send with response
            response.data["token"] = token.key
            return response
        except:
            return Response(data={"responseCode": 0, "errorMessage": "User registration failed"},
                            status=status.HTTP_400_BAD_REQUEST)


# Updating at [/api/auth/update/<username> ], PUT, Authentication: Token
class UpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOnly]
    authentication_classes = [TokenAuthentication]
    lookup_field = "username"

    def update(self, request, *args, **kwargs):
        try:
            response = super(UpdateAPIView, self).update(request, *args, **kwargs)
            # Get the user to send with response
            user = User.objects.get(username=response.data['username'])
            profile = UserProfile.objects.get(user=user)
            response.data['responseCode'] = 1
            response.data['first_name'] = profile.first_name
            response.data['last_name'] = profile.last_name
            response.data['address'] = profile.address
            response.data['phone'] = profile.phone

            return response
        except:
            return Response(data={"responseCode": 0, "errorMessage": "User update failed"},
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_profile = UserProfile.objects.get(user=instance)
            # self.perform_destroy(user_profile)
            user_profile.is_active = False
            user_profile.save()
            self.perform_destroy(instance)
            return Response(data={"responseCode": 1, "successMessage": "success"}, status=status.HTTP_200_OK)
        except Http404:
            pass
        return Response(data={"responseCode": 0, "errorMessage": "no content"},
                        status=status.HTTP_204_NO_CONTENT)


class LoginAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            user = User.objects.get(username=response.data['username'])
            token = Token.objects.get(user=user)  # Get token of the user and send with response
            response.data["token"] = token.key
            response.data['responseCode'] = 1
            return response

        except:
            return Response(data={"responseCode": 0, "errorMessage": "User does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)
