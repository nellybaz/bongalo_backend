from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


def check_token_authorization(user, request):
    if request.META.get('HTTP_AUTHORIZATION'):
        request_token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        token = Token.objects.get(key=request_token[1])
        print(token.key)
        if token.user != user:
            return False

    return True
