from apartment.serializers import ReviewSerializer
from rest_framework.views import APIView
from apartment.models import Apartment, Review
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User


class ReviewListUpdateCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_param = self.request.query_params.get("apartment") or None

        # Check error in query params
        if not query_param:
            response_data = {
                "responseCode": 0,
                "data": "bad query params",
                "message": "bad query params"
            }
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        # Check if the apartment exits
        if not Apartment.objects.filter(uuid=query_param).exists():
            response_data = {
                "responseCode": 0,
                "data": "apartment does not exists",
                "message": "apartment does not exists"
            }
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        apartment = Apartment.objects.get(uuid=query_param)
        query_set = Review.objects.filter(apartment=apartment, is_active=True)
        serialized = ReviewSerializer(query_set, many=True)
        if serialized:
            response_data = {
                "responseCode": 1,
                "data": serialized.data
            }
            return Response(data=response_data, status=status.HTTP_200_OK)

        response_data = {
            "responseCode": 0,
            "data": serialized.errors,
            'message': 'Error occurred'
        }
        return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serialized = ReviewSerializer(
            data=request.data, context={
                "request": "post"})
        if serialized.is_valid():
            serialized.save()
            response_data = {
                "responseCode": 1,
                "data": serialized.data
            }
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        response_data = {
            "responseCode": 0,
            "data": serialized.errors,
            'message': 'Error occurred'
        }
        return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        _review_exists = Review.objects.filter(uuid=request.data['uuid'])
        if _review_exists.exists():
            review = Review.objects.get(uuid=request.data['uuid'])

            # Check if person deleting made the review
            user_exists = User.objects.filter(
                username=request.data['given_by'])
            if not user_exists.exists():
                response_data = {
                    "statusCode": 0,
                    "data": "user does not exits",
                    'message': "user does not exits",
                }
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(username=request.data['given_by'])

            if review.given_by != user:
                response_data = {
                    "statusCode": 0,
                    "data": "user cannot delete the review",
                    "message": "user cannot delete the review",
                }
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

            if review.is_active:
                review.is_active = False
                review.save()
                response_data = {
                    "statusCode": 1,
                    "data": "review deleted successfully",
                }
                return Response(data=response_data, status=status.HTTP_200_OK)
            response_data = {
                "statusCode": 0,
                "data": "review already deleted",
                "message": "review already deleted",
            }
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            "statusCode": 0,
            "data": "review does not exists",
            "message": "review does not exists"
        }

        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
