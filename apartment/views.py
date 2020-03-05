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


# TODO: Apartment creation owner parameter must match the authenticated user
# TODO: Implement number of views for an apartment
# TODO: Password Validation on the backend
# TODO: Ask traveller phone submission when making reservations
# TODO: Available from/to dates, check-in/to times
# TODO: Searching with location and available dates, filtering with check-in/out times
# TODO: Apartment ratings
# TODO: Host [apartment listing *** priority]
# TODO:
# TODO:
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
            serialized = ApartmentSerializer(apartment, data=request.data, context={"request": "put"}, partial=True)
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
        serialized = ApartmentSerializer(data=request.data, context={"request": "post"})
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
    queryset = Apartment.objects.all()


# Receives location, check_in, check_out and returns filtered query
class ApartmentSearchAPIView(ListAPIView):
    serializer_class = ApartmentSerializer

    def get_queryset(self):
        country = self.request.query_params.get("country")  # Is mandatory field for search
        available_from = self.request.query_params.get("available-from")
        available_to = self.request.query_params.get("available-to")

        if available_from and available_to:
            return Apartment.objects.filter(country=country, available_from__gte=available_from, available_to__lte=available_to)
        elif available_from and not available_to:
            return Apartment.objects.filter(country=country, available_from__gte=available_from)
        elif available_to and not available_from:
            return Apartment.objects.filter(country=country, available_to__lte=available_to)
        else:
            return Apartment.objects.filter(country=country)


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
        serialized = ReviewSerializer(data=request.data, context={"request": "post"})
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
            user_exists = User.objects.filter(username=request.data['given_by'])
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
        serialized = ImageSerializer(data=request.data, context={"request": "post"})
        if serialized.is_valid():
            serialized.save()

            response_data = {"responseCode": 1, "data": serialized.data}
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        response_data = {"responseCode": 0, "data": serialized.errors}
        return Response(data=response_data, status=status.HTTP_200_OK)

    def get(self, request):
        apartment = self.request.query_params.get("apartment")
        if not Apartment.objects.filter(uuid=apartment).exists():

            response_data = {"responseCode": 0, "data": "apartment does not exist"}
            return Response(data=response_data, status=status.HTTP_200_OK)

        apartment_obj = Images.objects.filter(apartment=apartment)
        serialized = ImageSerializer(apartment_obj, context={"request": "post"}, many=True)
        if serialized:

            response_data = {"responseCode": 1, "data": serialized.data}
            return Response(data=response_data, status=status.HTTP_200_OK)

        response_data = {"responseCode": 0, "data": serialized.errors}
        return Response(data=response_data, status=status.HTTP_200_OK)


class BookingView(APIView):
    def post(self, request):
        serialized = BookingSerializer(data=request.data, context={"request": "post"})
        if serialized.is_valid():
            serialized.save()

            response_data = {"responseCode": 1, "data": serialized.data}
            return Response(data=response_data, status=status.HTTP_200_OK)

        response_data = {"responseCode": 0, "data": serialized.errors}
        return Response(data=response_data, status=status.HTTP_200_OK)


class RatingView(APIView):
    def post(self, request):
        serialized = RatingSerializer(data=request.data, context={"request": "post"})
        if serialized.is_valid():
            serialized.save()
            
            response = {

            }