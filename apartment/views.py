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
# TODO:
# TODO:
# TODO:
# TODO:
# TODO:

class ApartmentUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOnly]
    authentication_classes = [TokenAuthentication]
    serializer_class = ApartmentSerializer
    queryset = Apartment.objects.all()
    lookup_field = "uid"


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
        location = self.request.query_params.get("location")  # Is mandatory field for search
        check_in = self.request.query_params.get("check_in")
        check_out = self.request.query_params.get("check_out")

        if check_in and check_out:
            return Apartment.objects.filter(location=location, check_in__lte=check_in, check_out__gte=check_out)
        elif check_in and not check_out:
            return Apartment.objects.filter(location=location, check_in__lte=check_in)
        elif check_out and not check_in:
            return Apartment.objects.filter(location=location, check_out__gte=check_out)
        else:
            return Apartment.objects.filter(location=location)


class ReviewListUpdateCreate(ListAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
