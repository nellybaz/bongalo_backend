from apartment.serializers import ApartmentSerializer, ReviewSerializer, ImageSerializer, BookingSerializer, RatingSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from apartment.models import Apartment, Review, Images
from rest_framework.permissions import IsAuthenticated
from apartment.permissions import IsOwnerOrReadOnly as IsOwnerOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import datetime as dt
from authentication.models import UserProfile


# TODO: Implement number of views for an apartment
# TODO: Ask traveller phone submission when making reservations
# TODO: Apartment ratings
# TODO: Guest can see open bookings and can cancel
# TODO: Create events and experience model
# TODO:
# TODO:
# TODO:


class ApartmentUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOnly]
    authentication_classes = [TokenAuthentication]

    # serializer_class = ApartmentSerializer
    #     # queryset = Apartment.objects.all()
    #     # lookup_field = "uid"

    def put(self, request):
        apartment_uuid = request.data.pop('uuid')
        apartment_exists = Apartment.objects.filter(uuid=apartment_uuid)
        if apartment_exists.exists():
            apartment = Apartment.objects.get(uuid=apartment_uuid)
            serialized = ApartmentSerializer(
                apartment, data=request.data, context={
                    "request": "put"}, partial=True)
            if serialized.is_valid():
                serialized.save()
                response_data = {
                    "statusCode": 1,
                    "data": serialized.data
                }

                return Response(data=response_data, status=status.HTTP_200_OK)
            response_data = {
                "statusCode": 0,
                "data": serialized.errors
            }

            return Response(data=response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                "statusCode": 0,
                "data": "apartment does not exists"
            }

            return Response(data=response_data, status=status.HTTP_200_OK)

    def delete(self, request):
        print("delete called")
        _apartment_exists = Apartment.objects.filter(uuid=request.data['uuid'])
        if _apartment_exists.exists():
            apartment = Apartment.objects.get(uuid=request.data['uuid'])
            if apartment.is_active:
                apartment.is_active = False
                apartment.save()
                response_data = {
                    "statusCode": 1,
                    "data": "apartment deleted successfully",
                }
                return Response(data=response_data, status=status.HTTP_200_OK)
            response_data = {
                "statusCode": 0,
                "data": "apartment already deleted",
            }
            return Response(data=response_data, status=status.HTTP_200_OK)

        response_data = {
            "statusCode": 0,
            "data": "apartment does not exists"
        }

        return Response(data=response_data, status=status.HTTP_200_OK)


class ApartmentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOnly]
    authentication_classes = [TokenAuthentication]

    # serializer_class = ApartmentSerializer
    # queryset = Apartment.objects.all()

    def post(self, request):
        serialized = ApartmentSerializer(
            data=request.data, context={
                "request": "post"})
        if serialized.is_valid():
            serialized.save()
            response_data = {
                "statusCode": 1,
                "data": serialized.data,
            }
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        response_data = {
            "statusCode": 0,
            "data": serialized.errors
        }

        return Response(data=response_data, status=status.HTTP_200_OK)


class ApartmentListAPIView(ListAPIView):
    serializer_class = ApartmentSerializer
    queryset = Apartment.objects.filter(is_active=True, is_available=True)


# Receives location, check_in, check_out and returns filtered query
class ApartmentSearchAPIView(APIView):

    def get(self, request):
        apartment_type = self.request.query_params.get("type")
        check_in = self.request.query_params.get("checkin")
        check_out = self.request.query_params.get("checkout")
        number_of_guest = self.request.query_params.get("guest")
        result = []

        # No checkout, no checkin and apartment type is all
        if not check_out and not check_in and apartment_type == "all":
            result = Apartment.objects.filter(
                is_available=True,
                max_guest_number__gte=number_of_guest,
                is_active=True)
            serialized = ApartmentSerializer(result, many=True)
            response = {
                'responseCode': 1,
                'count': len(serialized.data),
                'results': serialized.data
            }
            return Response(data=response, status=status.HTTP_200_OK)

        # No checkout, no checkin and apartment type is not all
        if not check_out and not check_in and apartment_type != "all":
            result = Apartment.objects.filter(
                space=apartment_type,
                is_available=True,
                max_guest_number__gte=number_of_guest,
                is_active=True)
            serialized = ApartmentSerializer(result, many=True)
            response = {
                'responseCode': 1,
                'count': len(serialized.data),
                'results': serialized.data
            }
            return Response(data=response, status=status.HTTP_200_OK)

        if check_in and check_out and apartment_type == "all":
            res = []
            all_apartment = Apartment.objects.filter(
                is_available=True, max_guest_number__gte=number_of_guest, is_active=True)
            for apartment in all_apartment:
                d_apartment = apartment
                check_out_d = dt.datetime.strptime(
                    check_out + ' 00:00:00', '%d/%m/%Y %H:%M:%S')
                check_in_d = dt.datetime.strptime(
                    check_in + ' 00:00:00', '%d/%m/%Y %H:%M:%S')
                if check_out_d.date() < d_apartment.unavailable_from or check_in_d.date(
                ) > d_apartment.unavailable_to:
                    res.append(d_apartment.uuid)

            result = Apartment.objects.filter(uuid__in=res)
            serialized = ApartmentSerializer(result, many=True)
            response = {
                'responseCode': 1,
                'count': len(serialized.data),
                'results': serialized.data
            }
            return Response(data=response, status=status.HTTP_200_OK)

        if check_in and check_out and apartment_type != "all":
            res = []
            all_apartment = Apartment.objects.filter(
                space=apartment_type,
                is_available=True,
                max_guest_number__gte=number_of_guest,
                is_active=True)
            for apartment in all_apartment:
                d_apartment = apartment
                check_out_d = dt.datetime.strptime(
                    check_out + ' 00:00:00', '%d/%m/%Y %H:%M:%S')
                check_in_d = dt.datetime.strptime(
                    check_in + ' 00:00:00', '%d/%m/%Y %H:%M:%S')
                if check_out_d.date() < d_apartment.unavailable_from or check_in_d.date(
                ) > d_apartment.unavailable_to:
                    res.append(d_apartment.uuid)

            result = Apartment.objects.filter(uuid__in=res)
            serialized = ApartmentSerializer(result, many=True)
            response = {
                'responseCode': 1,
                'count': len(serialized.data),
                'results': serialized.data
            }
            return Response(data=response, status=status.HTTP_200_OK)

        response = {
            'responseCode': 1,
            'count': 0,
            'results': []
        }
        return Response(data=response, status=status.HTTP_200_OK)


class ReviewListUpdateCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_param = self.request.query_params.get("apartment") or None

        # Check error in query params
        if not query_param:
            response_data = {
                "responseCode": 0,
                "data": "bad query params"
            }
            return Response(data=response_data, status=status.HTTP_200_OK)

        # Check if the apartment exits
        if not Apartment.objects.filter(uuid=query_param).exists():
            response_data = {
                "responseCode": 0,
                "data": "apartment does not exists"
            }
            return Response(data=response_data, status=status.HTTP_200_OK)

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
            "data": serialized.errors
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

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
            "data": serialized.errors
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

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
                }
                return Response(data=response_data, status=status.HTTP_200_OK)

            user = User.objects.get(username=request.data['given_by'])

            if review.given_by != user:
                response_data = {
                    "statusCode": 0,
                    "data": "user cannot delete the review",
                }
                return Response(data=response_data, status=status.HTTP_200_OK)

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
            }
            return Response(data=response_data, status=status.HTTP_200_OK)

        response_data = {
            "statusCode": 0,
            "data": "review does not exists"
        }

        return Response(data=response_data, status=status.HTTP_200_OK)


class ImageView(APIView):
    def post(self, request):
        serialized = ImageSerializer(
            data=request.data, context={
                "request": "post"})
        if serialized.is_valid():
            serialized.save()

            response_data = {"responseCode": 1, "data": serialized.data}
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        response_data = {"responseCode": 0, "data": serialized.errors}
        return Response(data=response_data, status=status.HTTP_200_OK)

    def get(self, request):
        apartment = self.request.query_params.get("apartment")
        if not Apartment.objects.filter(uuid=apartment).exists():

            response_data = {
                "responseCode": 0,
                "data": "apartment does not exist"}
            return Response(data=response_data, status=status.HTTP_200_OK)

        apartment_obj = Images.objects.filter(apartment=apartment)
        serialized = ImageSerializer(
            apartment_obj, context={
                "request": "post"}, many=True)
        if serialized:

            response_data = {"responseCode": 1, "data": serialized.data}
            return Response(data=response_data, status=status.HTTP_200_OK)

        response_data = {"responseCode": 0, "data": serialized.errors}
        return Response(data=response_data, status=status.HTTP_200_OK)


class BookingView(APIView):
    def post(self, request):
        serialized = BookingSerializer(
            data=request.data, context={
                "request": "post"})
        if serialized.is_valid():
            serialized.save()

            response_data = {"responseCode": 1, "data": serialized.data}
            return Response(data=response_data, status=status.HTTP_200_OK)

        response_data = {"responseCode": 0, "data": serialized.errors}
        return Response(data=response_data, status=status.HTTP_200_OK)


class RatingView(APIView):
    def post(self, request):
        serialized = RatingSerializer(
            data=request.data, context={
                "request": "post"})
        if serialized.is_valid():
            serialized.save()

            response = {

            }


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
            "data": "user does not exists"
        }
        return Response(data=response, status=status.HTTP_200_OK)

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
                "data": "apartment is not owned by this user"
            }
            return Response(data=response, status=status.HTTP_200_OK)

        response = {
            "responseCode": 0,
            "data": "user does not exists"
        }
        return Response(data=response, status=status.HTTP_200_OK)

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
                "data": "apartment is not owned by this user"
            }
            return Response(data=response, status=status.HTTP_200_OK)

        response = {
            "responseCode": 0,
            "data": "user does not exists"
        }
        return Response(data=response, status=status.HTTP_200_OK)
