from apartment.serializers import ApartmentSerializer
from rest_framework.views import APIView
from apartment.models import Apartment
from rest_framework.response import Response
from rest_framework import status
from authentication.models import UserProfile


class ListingView(APIView):
    def get(self, request):
        user_id = self.request.query_params.get('user')
        if UserProfile.objects.filter(uuid=user_id).exists():
            user = UserProfile.objects.get(uuid=user_id)
            serialized = ApartmentSerializer(
                Apartment.objects.filter(
                    owner=user, is_active=True), many=True)
            if serialized:
                response = {
                    "responseCode": 1,
                    "count": len(serialized.data),
                    "data": serialized.data
                }
            return Response(data=response, status=status.HTTP_200_OK)

        response = {
            "responseCode": 0,
            "data": "user does not exists",
            "message": "user does not exists",
        }
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_id = self.request.query_params.get('user')
        apartment_id = self.request.query_params.get('apartment')
        if UserProfile.objects.filter(uuid=user_id).exists():
            user = UserProfile.objects.get(uuid=user_id)
            apartment = Apartment.objects.get(uuid=apartment_id)

            if apartment.owner == user:
                apartment.is_active = False
                apartment.save()
                response = {
                    "responseCode": 1,
                    "data": "apartment deleted"
                }
                return Response(data=response, status=status.HTTP_200_OK)

            response = {
                "responseCode": 0,
                "data": "apartment is not owned by this user",
                "message": "apartment is not owned by this user"
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        response = {
            "responseCode": 0,
            "data": "user does not exists",
            "message": "user does not exists"
        }
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        user_id = request.data['user']
        apartment_id = request.data['apartment']
        if UserProfile.objects.filter(uuid=user_id).exits():
            user = UserProfile.objects.get(uuid=user_id)
            apartment = Apartment.objects.get(uuid=apartment_id)
            if apartment.owner == user:
                serialized = ApartmentSerializer(apartment, data=request.data)
                if serialized:
                    response = {
                        "responseCode": 1,
                        "data": serialized.data
                    }
                return Response(data=response, status=status.HTTP_200_OK)

            response = {
                "responseCode": 0,
                "data": "apartment is not owned by this user",
                "message": "apartment is not owned by this user"
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        response = {
            "responseCode": 0,
            "data": "user does not exists",
            "message": "user does not exists"
        }
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
