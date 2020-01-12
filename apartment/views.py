from apartment.serializers import ApartmentSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from apartment.models import Apartment
from rest_framework.permissions import IsAuthenticated
from apartment.permissions import IsOwnerOrReadOnly as IsOwnerOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status


class ApartmentUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOnly]
    authentication_classes = [TokenAuthentication]
    serializer_class = ApartmentSerializer
    queryset = Apartment.objects.all()
    lookup_field = "uid"

    # def delete(self, request, *args, **kwargs):
    #     try:
    #         response = super().delete(request, *args, **kwargs)
    #         response.data['responseCode'] = 1
    #         return response
    #     except:
    #         return Response(data={"responseCode": 0, "errorMessage": "Delete operation failed"},
    #                         status=status.HTTP_400_BAD_REQUEST)


class ApartmentCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOnly]
    authentication_classes = [TokenAuthentication]
    serializer_class = ApartmentSerializer
    queryset = Apartment.objects.all()


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

