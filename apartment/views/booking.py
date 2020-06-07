from apartment.serializers import BookingSerializer, BookingWithApartmentSerializer
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView, ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from authentication.permissions import IsOwner
from rest_framework import status
from apartment.models import Booking, Apartment
from authentication.models import UserProfile
from rest_framework.response import Response
from payment.views import PaymentGateWay
from datetime import datetime

from utils.email_thread import EmailService, SendEmailThread


class CreateBookingView(ListCreateAPIView):
    write_serializer_class = BookingSerializer
    read_serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    queryset = Booking.objects.filter(is_active=True).all()

    def get_pay_url(self, payload):
        payment_gateway = PaymentGateWay()
        res = payment_gateway.create_token(payload)
        print('this,', 10 * "===")
        token = res.content.decode()
        print("token is hererrrrrrrreeeeeeee=====>>>>>>>>>>")
        print(token)
        token = token.split('<TransToken>')[1]
        token = token.split('</TransToken>')[0]
        redirect_url = 'https://secure.3gdirectpay.com/dpopayment.php?ID=' + token

        return {'token': token, 'redirect_url': redirect_url}

    def create(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        apartment = Apartment.objects.get(uuid=request.data.get("apartment"))
        user = UserProfile.objects.get(user=request.user)
        payment_description = 'Payment for booking of {0} from {1} to {2}'.format(apartment.title,
                                                                                  request.data.get('date_from'),
                                                                                  request.data.get('date_to'))
        date = datetime.now().date()
        date_arr = str(date).split("-")
        payload = {
            'amount': request.data.get("amount"),
            'description': payment_description,
            'first_name': user.user.first_name,
            'last_name': user.user.last_name,
            'phone_number': user.phone,
            'country_code': '250',
            'user_city': user.resident_city,
            'user_country': "rw",
            'user_email': user.user.email,
            'currency': 'usd',
            'redirect_url': request.data.get('redirect_url'),
            'back_url': request.data.get("back_url"),
            'transaction_limit': '1',
            'transaction_type': 'hours',
            # 'company_token': '22EEF8E8-C756-496E-BD68-EDAEF2741FB0',
            'company_token': '108B9501-5BC1-474A-954F-240CD2616D4C',
            'company_ref': 'SDGSDFGE5646345',
            'service_type': '36821',
            'service_date': '{}/{}/{}'.format(date_arr[0], date_arr[1], date_arr[2])

        }

        response_code = 0
        response_message = "Booking was successfully created"
        pay_url_data = {}
        response_status = status.HTTP_201_CREATED
        try:
            pay_url_data = self.get_pay_url(payload)
            response_code = 1
        except Exception as exc:
            print(exc, '=====')
            response_message = "Booking unsuccessful"
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            pass

        return Response(
            {'responseCode': response_code, 'booking': serializer.data, **pay_url_data, 'message': response_message},
            status=response_status,
            headers=headers)


class RetrieveDeleteBookingDetailsAPIView(RetrieveDestroyAPIView):
    queryset = Booking.objects.filter(is_active=True).all()
    serializer_class = BookingSerializer
    lookup_field = 'uuid'
    permission_classes = (IsAuthenticated, IsOwner)
    authentication_classes = [TokenAuthentication, ]

    def delete(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        booking = Booking.objects.get(client=user_profile, uuid=self.kwargs.get('uuid'))
        booking.is_active = False
        booking.save()
        serializer = self.get_serializer_class()
        serialized_data = serializer(booking)
        host = booking.apartment.owner.user
        cancel_by = request.user.email
        guest = booking.client.user

        try:
            guest_email_service = EmailService(guest.email)
            host_email_service = EmailService(host.email)
            admin_email_service = EmailService('info@bongalo.co')
            payload = {
                'host_last_name': host.last_name,
                'client_last_name': guest.last_name,
                'host_first_name': host.first_name,
                'client_first_name': guest.first_name,
                'reference_number': booking.uuid

            }
            if guest.email == cancel_by.email:
                emails_to_send = [guest_email_service.cancelation_by_guest_to_guest,
                                  host_email_service.cancelation_by_guest_to_host,
                                  admin_email_service.cancelation_by_guest_to_admin]
                for email in emails_to_send:
                    email_thread = SendEmailThread(email, payload=payload)
                    email_thread.run()
            elif host.email == cancel_by.email:
                emails_to_send = [guest_email_service.cancelation_by_host_to_guest,
                                  host_email_service.cancelation_by_host_to_host,
                                  admin_email_service.cancelation_by_host_to_admin]
                for email in emails_to_send:
                    email_thread = SendEmailThread(email, payload=payload)
                    email_thread.run()
        except BaseException as e:
            print(str(e))

        return Response(
            {'responseCode': 1, 'data': serialized_data.data, 'message': 'your booking was canceled'},
            status=status.HTTP_204_NO_CONTENT)


class MyBooking(APIView):
    """
    get bookings made by a client and on his apartment
    """
    serializer_class = BookingWithApartmentSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)
        my_booking = Booking.objects.filter(is_active=True, client=user_profile)
        booking_on_my_apartment = Booking.objects.filter(apartment__owner=user_profile, is_active=True)
        serialized_my_booking = self.serializer_class(my_booking, many=True)
        serialized_booking_on_my_apartment = self.serializer_class(booking_on_my_apartment, many=True)
        return Response(
            {'responseCode': 1,
             'data': {
                 'my_booking': serialized_my_booking.data,
                 'booking_on_my_apartment': serialized_booking_on_my_apartment.data
             },
             'message': 'your booking was retrieved'},
            status=status.HTTP_200_OK)

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        return Booking.objects.filter(is_active=True, client=user_profile)


class BookingOnMyApartment(ListAPIView):
    """
    get bookings made on a client apartment
    """
    serializer_class = BookingWithApartmentSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    authentication_classes = [TokenAuthentication, ]

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        return Booking.objects.filter(apartment__owner=user_profile, is_active=True)
