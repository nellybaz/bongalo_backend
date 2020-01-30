from apartment.serializers import ApartmentSerializer, ReviewSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from apartment.models import Apartment, Review
from rest_framework.permissions import IsAuthenticated
from apartment.permissions import IsOwnerOrReadOnly as IsOwnerOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status


# TODO: Login username get parameter must match authentication username
# TODO: Apartment creation owner parameter must match the authenticated user
# TODO: Implement number of views for an apartment
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
            serialized = ApartmentSerializer(apartment, data=request.data, context={"request": "put"})
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

            return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            response_data = {
                "statusCode": 0,
                "data": "apartment does not exists"
            }

            return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

        return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApartmentListAPIView(ListAPIView):
    serializer_class = ApartmentSerializer
    queryset = Apartment.objects.all()


# Receives location, check_in, check_out and returns filtered query
class ApartmentSearchAPIView(ListAPIView):
    serializer_class = ApartmentSerializer

    def get_queryset(self):
        country = self.request.query_params.get("location")  # Is mandatory field for search
        check_in = self.request.query_params.get("check_in")
        check_out = self.request.query_params.get("check_out")

        if check_in and check_out:
            return Apartment.objects.filter(country=country, check_in__lte=check_in, check_out__gte=check_out)
        elif check_in and not check_out:
            return Apartment.objects.filter(country=country, check_in__lte=check_in)
        elif check_out and not check_in:
            return Apartment.objects.filter(country=country, check_out__gte=check_out)
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
            return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Check if the apartment exits
        if not Apartment.objects.filter(uuid=query_param).exists():
            response_data = {
                "responseCode": 0,
                "data": "apartment does not exists"
            }
            return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        _review_exists = Review.objects.filter(uuid=request.data['uuid'])
        if _review_exists.exists():
            review = Review.objects.get(uuid=request.data['uuid'])
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
            return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_data = {
            "statusCode": 0,
            "data": "review does not exists"
        }

        return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
