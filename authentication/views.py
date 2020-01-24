from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView
# from .serializers import UserSerializer, ProfileSerializer
from .serializers import UserSerializer
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


class UserRegisterViews(APIView):
    def post(self, request):  # Handle user registration
        serialized = UserSerializer(data=request.data, context={"request": "post"})
        if serialized.is_valid():
            serialized.save()
            response_data = {'responseCode': 1, 'data': serialized.data}
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        response_data = {'responseCode': 0, 'data': serialized.errors}
        return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserUpdateView(APIView):
    permission_classes = [IsOwnerOnly, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self, request):
        is_exists = User.objects.filter(username=request.data['username'])
        if is_exists.exists():  # Update data if user exists
            user = User.objects.get(username=request.data['username'])
            print(request)
            self.check_object_permissions(request, user)
            serialized = UserSerializer(user, data=request.data, context={"request": "put"})
            if serialized.is_valid():
                serialized.save()
                response_data = {'responseCode': 1, 'data': serialized.data}
                return Response(data=response_data, status=status.HTTP_201_CREATED)
                # serialized.errors["responseCode"] = 0
            response_data = {'responseCode': 0, 'data': serialized.errors}
            return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response_data = {'responseCode': 0, 'data': {"error": "user does not exists"}}
            return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        is_exists = User.objects.filter(username=request.data['username'])
        if is_exists.exists():
            user = User.objects.get(username=request.data['username'])
            if user.is_active:
                user.is_active = False
                user.save()
                response_data = {'responseCode': 1, 'data': {"message": "Deleted successfully"}}
                return Response(data=response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {'responseCode': 0, 'data': {"error": "This User does not exists anymore"}}
                return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response_data = {'responseCode': 0, 'data': {"error": "User does not exists"}}
            return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

