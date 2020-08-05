from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import datetime as dt

from utils.email_thread import SendEmailThread, EmailService
from authentication.serializers import UserProfileSerializer
from apartment.permissions import IsOwnerOrReadOnly as IsOwnerOnly
from apartment.models import Apartment, Booking
from apartment.serializers import ApartmentSerializer


# TODO: Implement number of views for an apartment
# TODO: Ask traveller phone submission when making reservations
# TODO: Apartment ratings
# TODO: Guest can see open bookings and can cancel
# TODO: Create events and experience model

class ApartmentDetailsView(APIView):
    def get(self, request):
        apartment_uuid = self.request.query_params.get('uuid')
        apartment_exists = Apartment.objects.filter(uuid=apartment_uuid,
                                                    is_active=True)
        if apartment_exists.exists():
            apartment = Apartment.objects.get(uuid=apartment_uuid,
                                              is_active=True)
            owner_details_serialized = UserProfileSerializer(apartment.owner)
            serialized = ApartmentSerializer(
                apartment)
            if serialized and owner_details_serialized:
                all_bookings_for_apartment = Booking.objects.filter(
                    apartment=apartment, is_completed=True, is_active=True)
                unavailable_dates_for_apartment = []
                today = datetime.now().date()

                if "full_place" in apartment.space:
                    for booking in all_bookings_for_apartment:
                        if (booking.date_from > today
                           or today < booking.date_to):
                            unavailable_dates_for_apartment.append
                            ({"from": booking.date_from,
                             "to": booking.date_to})

                elif "private_room" in apartment.space:
                    booking_counts = []
                    for booking in all_bookings_for_apartment:
                        if (booking.date_from > today
                           or today < booking.date_to):
                            booking_counts.append(
                                {"from": booking.date_from,
                                 "to": booking.date_to})
                    if (len(booking_counts)
                            >= apartment.available_rooms):
                        unavailable_dates_for_apartment = booking_counts

                response_data = {
                    "responseCode": 1,
                    "data": {**serialized.data,
                             "owner_details":
                             {**owner_details_serialized.data},
                             "unavailable_dates":
                             unavailable_dates_for_apartment},
                    "message": "ok"
                }

                return Response(data=response_data, status=status.HTTP_200_OK)
            response_data = {
                "responseCode": 0,
                "data": serialized.errors,
                'message': 'Error occurred'
            }

            return Response(data=response_data,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            response_data = {
                "responseCode": 0,
                "data": "apartment does not exists",
                "message": "apartment does not exists"
            }

            return Response(data=response_data,
                            status=status.HTTP_404_NOT_FOUND)


class ApartmentUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOnly]
    authentication_classes = [TokenAuthentication]

    def put(self, request):
        apartment_uuid = request.data.pop('uuid')
        # TODO:  what happens when when I am not an owner
        apartment_exists = Apartment.objects.filter(uuid=apartment_uuid)
        if apartment_exists.exists():
            apartment = Apartment.objects.get(uuid=apartment_uuid)
            serialized = ApartmentSerializer(
                apartment, data=request.data, context={
                    "request": "put"}, partial=True)
            if serialized.is_valid():
                serialized.save()
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

            return Response(data=response_data,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            response_data = {
                "responseCode": 0,
                "data": "apartment does not exists",
                "message": "apartment does not exists"
            }

            return Response(data=response_data,
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        _apartment_exists = Apartment.objects.filter(uuid=request.data['uuid'])
        if _apartment_exists.exists():
            apartment = Apartment.objects.get(uuid=request.data['uuid'])
            if apartment.is_active:
                apartment.is_active = False
                apartment.save()
                response_data = {
                    "responseCode": 1,
                    "data": "apartment deleted successfully",
                }
                return Response(data=response_data, status=status.HTTP_200_OK)
            response_data = {
                "responseCode": 0,
                "data": "apartment already deleted",
                "message": "apartment already deleted",
            }
            return Response(data=response_data,
                            status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            "responseCode": 0,
            "data": "apartment does not exists",
            "message": "apartment does not exists"
        }

        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)


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

            try:
                email_service = EmailService(request.user.email)
                payload = {
                    'lastName': request.user.last_name,
                    # 'verification_pin': verification_pin
                }
                email_thread = SendEmailThread(
                    email_service.apartment_listing_confirmation,
                    payload=payload)
                email_thread.run()
            except BaseException as e:
                print(str(e))

            response_data = {
                "responseCode": 1,
                "data": serialized.data,
                "message": "Apartment created successfully"
            }
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        response_data = {
            "responseCode": 0,
            "data": serialized.errors,
            'message': 'Error occurred'
        }

        return Response(data=response_data,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApartmentListAPIView(ListAPIView):
    serializer_class = ApartmentSerializer
    queryset = Apartment.objects.filter(is_active=True, is_available=True)


# TODO : This need refractoring
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
                is_available=True,
                max_guest_number__gte=number_of_guest,
                is_active=True)
            for apartment in all_apartment:
                d_apartment = apartment
                check_out_d = dt.datetime.strptime(
                    check_out + ' 00:00:00', '%d/%m/%Y %H:%M:%S')
                check_in_d = dt.datetime.strptime(
                    check_in + ' 00:00:00', '%d/%m/%Y %H:%M:%S')
                if (check_out_d.date() < d_apartment.unavailable_from
                   or check_in_d.date(
                   ) > d_apartment.unavailable_to):
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
                if (check_out_d.date() < d_apartment.unavailable_from
                   or check_in_d.date(
                   ) > d_apartment.unavailable_to):
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
