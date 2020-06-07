from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from rest_framework import status
from apartment.models import Booking
from authentication.models import UserProfile
from utils.email_thread import SendEmailThread, EmailService


class PaymentGateWay(object):
    """this is the getKey function that generates an encryption Key for you by passing your Secret Key as a
    parameter. """

    def verify_token(self, token):
        url = 'https://secure.3gdirectpay.com/API/v6/'
        data = '<?xml version="1.0" encoding="utf-8"?><API3G><CompanyToken>22EEF8E8-C756-496E-BD68-EDAEF2741FB0' \
               '</CompanyToken><Request>verifyToken</Request><TransactionToken>' + token + '</TransactionToken></API3G> '
        headers = {'Content-Type': 'application/xml'}
        res = requests.post(url, data, headers)
        return res

    '''
    Payment for booking of {House name} from {date_from} to {date_to} 


    <?xml version="1.0" encoding="utf-8"?>
            <API3G>
                <CompanyToken>22EEF8E8-C756-496E-BD68-EDAEF2741FB0</CompanyToken>
                <Request>createToken</Request>
                <Transaction>
                    <customerFirstName>Alex</customerFirstName>
                    <customerLastName>Mathenge IV</customerLastName>
                    <customerPhone>9876543210</customerPhone>
                    <customerZip>254</customerZip>
                    <customerCity>Nairobi</customerCity>
                    <customerCountry>KE</customerCountry>
                    <customerEmail>nellybaz10@gmail.com</customerEmail>
                    <PaymentAmount>0.1</PaymentAmount>
                    <PaymentCurrency>usd</PaymentCurrency>
                    <CompanyRef>49FKEOA</CompanyRef>
                    <RedirectURL>https://bongalo-frontend.herokuapp.com</RedirectURL>
                    <BackURL>https://bongalo-frontend.herokuapp.com</BackURL>
                    <CompanyRefUnique>1</CompanyRefUnique>
                    <PTL>15</PTL>
                    <PTLtype>hours</PTLtype>
                </Transaction>
                <Services>
                    <Service>
                        <ServiceType>8162</ServiceType>
                        <ServiceDescription>Orders</ServiceDescription>
                        <ServiceDate>2020/04/29</ServiceDate>
                    </Service>
                </Services>
            </API3G>

    payload = {
            'amount': request.data.get("amount"),
            'description': payment_description,
            'first_name': user.user.first_name,
            'last_name': user.user.last_name,
            'phone_number': user.phone,
            'country_code': '250',
            'city': user.resident_city,
            'country': user.resident_country,
            'email': user.user.email,
            'currency': 'usd',
            'redirect_url': 'https://bongalo-frontend.herokuapp.com',
            'back_url': 'https://bongalo-frontend.herokuapp.com',
            'transaction_limit': '1',
            'transaction_type': 'hours',

        }
    '''

    def create_token(self, payload):
        url = 'https://secure.3gdirectpay.com/API/v6/'
        data = '<?xml version="1.0" encoding="utf-8"?><API3G><CompanyToken>'+payload.get('company_token')+'</CompanyToken><Request>createToken</Request><Transaction><customerFirstName>'+payload.get('first_name')+'</customerFirstName><customerLastName>'+payload.get('last_name')+'</customerLastName><customerPhone>'+payload.get('phone_number')+'</customerPhone><customerZip>'+payload.get('country_code')+'</customerZip><customerCity>'+payload.get('user_city')+'</customerCity><customerCountry>'+payload.get('user_country')+'</customerCountry><customerEmail>'+payload.get('user_email')+'</customerEmail><PaymentAmount>'+str(payload.get('amount'))+'</PaymentAmount><PaymentCurrency>'+payload.get('currency')+'</PaymentCurrency><CompanyRef>'+payload.get('company_ref')+'</CompanyRef><RedirectURL>'+payload.get('redirect_url')+'</RedirectURL><BackURL>'+payload.get('back_url')+'</BackURL><CompanyRefUnique>0</CompanyRefUnique><PTL>'+payload.get('transaction_limit')+'</PTL><PTLtype>'+payload.get('transaction_type')+'</PTLtype></Transaction><Services><Service><ServiceType>'+payload.get('service_type')+'</ServiceType><ServiceDescription>' + payload.get('description') + '</ServiceDescription><ServiceDate>'+payload.get('service_date')+'</ServiceDate></Service></Services></API3G>'
        headers = {'Content-Type': 'application/xml'}
        res = requests.post(url, data, headers)
        return res


'''

on pay redirect
if the booking is not paid and the token is same as the one sent, we mark booking paid, verify token and create payment 
object and then send a success/error message to determine response on the payment response page

'''


class PaymentView(APIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = .get(TokenAuthentication)

    def get(self, request):
        pass

    def post(self, request):
        user_id = request.data.get('user')
        user = UserProfile.objects.get(uuid=user_id, is_active=True)
        token = request.data.get('pay_token')
        user_booking = Booking.objects.filter(client=user).order_by('-created_at').first()
        payment_gateway = PaymentGateWay()

        if not user_booking.is_completed:
            user_booking.is_completed = True
            user_booking.save()

            # apartment = user_booking.apartment
            # if "private_room" in apartment.space:
            #     if len(Booking.objects.filter(apartment=apartment, is_completed=True)) == apartment.available_rooms:
            #         apartment.is_available = False
            #         apartment.save()
            #
            # else:
            #     apartment.is_available = False
            #     apartment.save()

            res = payment_gateway.verify_token(token).content.decode()
            print(res)

            if 'Transaction Paid' in res:
                try:
                    email_service = EmailService(user.user.email)
                    payload = {
                        'booking': user_booking,
                    }
                    email_thread = SendEmailThread(email_service.send_payment_confirmation, payload=payload)
                    email_thread.run()
                except BaseException as e:
                    print(str(e))

                try:
                    email_service = EmailService(user_booking.apartment.owner.user.email)
                    payload = {
                        'booking': user_booking,
                    }
                    email_thread = SendEmailThread(email_service.host_booking_notification, payload=payload)
                    email_thread.run()
                except BaseException as e:
                    print(str(e))

                return Response(data={'responseCode': 1, 'message': 'Paid completed'},
                                status=status.HTTP_200_OK)

            return Response(data={'responseCode': -1}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={'responseCode': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
