from django.http import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, VerifyUserSerializer
from django.contrib.auth.models import User
from .models import UserProfile
from authentication.permissions import IsOwnerOrReadOnly as IsOwnerOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from utils import check_token_autorization


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        print("username is {} and password is {}".format(username, password))
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            # check if user is active
            profile = UserProfile.objects.get(user=user)
            if profile.is_active:
                # Get token
                token = Token.objects.get(user=user)
                response_data = {'responseCode': 1, 'data': "login successful", "uuid": profile.uuid, "token": token.key}
                return Response(data=response_data, status=status.HTTP_200_OK)
            else:
                response_data = {'responseCode': 0, 'data': "user account is not active"}
                return Response(data=response_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        response_data = {'responseCode': 0, 'data': "login failed"}
        return Response(data=response_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class UserRegisterViews(APIView):
    def post(self, request):  # Handle user registration
        serialized = UserRegisterSerializer(data=request.data, context={"request": "post"}, partial=True)
        if serialized.is_valid():
            serialized.save()
            response_data = {'responseCode': 1, 'data': serialized.data}
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        response_data = {'responseCode': 0, 'data': serialized.errors}
        return Response(data=response_data, status=status.HTTP_200_OK)


class SocialAuth(APIView):
    def post(self, request):
        username = request.data['username']

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            # check if user is active
            profile = UserProfile.objects.get(user=user)
            if profile.is_active:
                # Get token
                token = Token.objects.get(user=user)
                response_data = {'responseCode': 1, 'data': "login successful", "uuid": profile.uuid, "token": token.key}
                return Response(data=response_data, status=status.HTTP_200_OK)
            else:
                response_data = {'responseCode': 0, 'data': "user does not exists anymore"}
                return Response(data=response_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        serialized = UserRegisterSerializer(data=request.data, context={"request": "post"}, partial=True)
        if serialized.is_valid():
            serialized.save()
            response_data = {'responseCode': 1, 'data': serialized.data}
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        response_data = {'responseCode': 0, 'data': serialized.errors}
        return Response(data=response_data, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    permission_classes = [IsOwnerOnly, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self, request):
        is_exists = User.objects.filter(username=request.data['username'])
        if is_exists.exists():  # Update data if user exists
            user = User.objects.get(username=request.data['username'])
            print(request)

            # Check if user can update account
            if not check_token_autorization.check_token_authorization(user, request):
                response_data = {'responseCode': 0, 'data': "This user cannot update this account"}
                return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.check_object_permissions(request, user)
            serialized = UserRegisterSerializer(user, data=request.data, context={"request": "put"})
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


class DeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        print("deleted called =======>")
        is_exists = User.objects.filter(username=request.data['username'])
        if is_exists.exists():
            user = User.objects.get(username=request.data['username'])
            profile = UserProfile.objects.get(user=user)

            # Check if user can update account
            if not check_token_autorization.check_token_authorization(user, request):
                response_data = {'responseCode': 0, 'data': "This user cannot update this account"}
                return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if profile.is_active:
                profile.is_active = False
                profile.save()
                response_data = {'responseCode': 1, 'data': {"message": "Deleted successfully"}}
                return Response(data=response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {'responseCode': 0, 'data': {"error": "This User does not exists anymore"}}
                return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response_data = {'responseCode': 0, 'data': {"error": "User does not exists"}}
            return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        if "national_id" not in request.data and "passport" not in request.data:
            response_data = {'responseCode': 0, 'data': "passport or national_id required"}
            return Response(data=response_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if not User.objects.filter(username=request.data['username']).exists():
            response_data = {'responseCode': 0, 'data': "user does not exits"}
            return Response(data=response_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        user = User.objects.get(username=request.data['username'])
        request.data.pop("username")
        print(request.data)
        serialized = VerifyUserSerializer(UserProfile.objects.get(user=user), data=request.data, context={"request": "put"}, partial=True)
        if serialized.is_valid():
            serialized.save()
            response_data = {'responseCode': 1, 'data': serialized.data}
            return Response(data=response_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        response_data = {'responseCode': 0, 'data': serialized.errors}
        return Response(data=response_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
