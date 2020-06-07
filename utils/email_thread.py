import threading
from django.core.mail import send_mail
from django.conf import settings
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Personalization, Email, Substitution

#
# def send_email(to, subject, message):
#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [to],
#         fail_silently=False,
#     )
#
#
# def send_email_with_template(recipient_email, recipient_name, ):
#     message = Mail(
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to_emails=recipient_email,
#         html_content='<strong>and easy to do anywhere, even with Python</strong>',
#     )
#
#     name_sub = Substitution("name", recipient_name)
#     sender_name_sub = Substitution("Sender_Name", "Bongalo Ltd")
#     message.add_substitution(name_sub)
#     message.add_substitution(sender_name_sub)
#
#     message.template_id = '1c0076ca-2632-4457-b292-273cd87100ba'
#
#     try:
#         print('sendgrid api key is {0}'.format(settings.SENDGRID_API_KEY))
#         sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
#         response = sendgrid_client.send(message)
#         print("response from sendgrid ======>>>>>>")
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#     except Exception as e:
#         print("sendgrid error here below ====>>>>>>")
#         print(e)


class SendEmailThread(threading.Thread):
    email_function = None
    payload = None

    def __init__(self, email_function, payload):
        threading.Thread.__init__(self)
        self.email_function = email_function
        self.payload = payload
        print("initing the thread")

    def run(self):
        # send_email(self.recipient, self.subject, self.message)
        # send_email_with_template()
        print("before running email function")
        self.email_function(self.payload)
        print("after running the email function")


class EmailService:
    message = None

    def __init__(self, recipient_email):
        self.message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=recipient_email,
            html_content='<strong>and easy to do anywhere, even with Python</strong>',
        )

        self.message.add_substitution(Substitution("Sender_Name", "Bongalo Ltd"))
        self.message.add_substitution(Substitution("Sender_Address", "KG 622 St"))
        self.message.add_substitution(Substitution("Sender_City", "Fair View Building"))
        self.message.add_substitution(Substitution("Sender_State", "Kigali"))
        self.message.add_substitution(Substitution("Sender_Zip", "5377"))

    def send_welcome(self, payload):
        self.message.add_substitution(Substitution("name", payload['recipient_name']))

        self.message.template_id = '1c0076ca-2632-4457-b292-273cd87100ba'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            return response
        except Exception as e:
            print("sendgrid error here below ====>>>>>>")
            print(e)
            raise e

    def send_registration_pin(self, payload):
        self.message.add_substitution(Substitution("lastName", payload['recipient_last_name']))
        self.message.add_substitution(Substitution('pinNumber', payload['verification_pin']))

        self.message.template_id = 'ff97b311-eb6c-4df7-b6a6-d11e2eb59dec'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            return response
        except Exception as e:
            print("sendgrid error here below ====>>>>>>")
            print(e)
            raise e

    def apartment_listing_confirmation(self, payload):
        self.message.add_substitution(Substitution("lastName", payload['lastName']))

        self.message.template_id = 'b3e0163a-6080-4e2c-b4b4-9d744796e6b6'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            return response
        except Exception as e:
            print("sendgrid error here below ====>>>>>>")
            print(e)
            raise e

    def password_change(self, payload):
        self.message.add_substitution(Substitution("lastName", payload['lastName']))

        self.message.template_id = 'd56910c1-8e37-4e6d-b6b2-bfd86ea02ddd'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            return response
        except Exception as e:
            print("sendgrid error here below ====>>>>>>")
            print(e)
            raise e

    def newsletter_subscription(self, payload):
        # self.message.add_substitution(Substitution("lastName", payload['lastName']))

        self.message.template_id = '59c157a6-a911-4954-879e-b55bd31c954d'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            return response
        except Exception as e:
            print("sendgrid error here below ====>>>>>>")
            print(e)
            raise e

    def host_booking_notification(self, payload):

        date_from = str(payload['booking'].date_from)[0:10]
        date_to = str(payload['booking'].date_to)[0:10]

        self.message.add_substitution(Substitution("lastName", payload['booking'].apartment.owner.user.last_name))
        self.message.add_substitution(Substitution("guestFullName", "{0} {1}".format(payload['booking'].client.user.first_name, payload['booking'].client.user.last_name)))
        self.message.add_substitution(Substitution("referenceNumber", payload['booking'].uuid))
        self.message.add_substitution(Substitution("dateFrom", date_from))
        self.message.add_substitution(Substitution("dateTo", date_to))
        self.message.add_substitution(Substitution("guestEmail", payload['booking'].client.user.email))

        self.message.template_id = '8bfc2d14-588b-4678-acd1-00f0c47a2f2e'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            return response
        except Exception as e:
            print("sendgrid error here below ====>>>>>>")
            print(e)
            raise e

    def send_payment_confirmation(self, payload):
        booked_nights = 1
        try:
            booked_nights = abs((payload['booking'].date_from - payload['booking'].date_to).days)
            print("correct booked nights is {0}".format(booked_nights))
        except BaseException as e:
            print("wrong booked nights and error is {0}".format(str(e)))

        apartment_price = payload['booking'].apartment.price
        service_fee = (booked_nights * apartment_price) * 0.05

        date_from = str(payload['booking'].date_from)[0:10]
        date_to = str(payload['booking'].date_to)[0:10]
        created_at = str(payload['booking'].created_at)[0:10]

        self.message.add_substitution(Substitution("lastName", payload['booking'].client.user.last_name))
        self.message.add_substitution(Substitution('nameOfPlace', payload['booking'].apartment.title))
        self.message.add_substitution(Substitution('hostEmail', payload['booking'].apartment.owner.user.email))
        self.message.add_substitution(Substitution('nameOfHost', "{0} {1}".format(payload['booking'].apartment.owner.user.first_name, payload['booking'].apartment.owner.user.last_name,)))
        self.message.add_substitution(Substitution('dateOfPayment', created_at))
        self.message.add_substitution(Substitution('bookingReference', payload['booking'].uuid))

        self.message.add_substitution(Substitution('clientName', "{0} {1}".format(payload['booking'].client.user.first_name, payload['booking'].client.user.last_name,)))
        self.message.add_substitution(Substitution('dateFrom', date_from))
        self.message.add_substitution(Substitution('dateTo', date_to))
        self.message.add_substitution(Substitution('checkinTime', payload['booking'].apartment.check_in))
        self.message.add_substitution(Substitution('checkoutTime', payload['booking'].apartment.check_out))

        # self.message.add_substitution(Substitution('apartmentName', payload['booking'].apartment.title))
        self.message.add_substitution(Substitution('price', str(apartment_price)))
        self.message.add_substitution(Substitution('numberOfNight', str(booked_nights)))
        self.message.add_substitution(Substitution('serviceFee', str(service_fee)))

        self.message.add_substitution(Substitution('total', str(service_fee + apartment_price)))

        self.message.template_id = '7e8da248-c9c0-4a7a-84b0-0e805c7f5fe6'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            return response
        except Exception as e:
            print("sendgrid error here below ====>>>>>>")
            print(e)
            raise e


    def cancelation_by_host_to_host(self, payload):
        self.message.add_substitution(Substitution("hostLastName", payload.get('host_last_name')))
        self.message.add_substitution(Substitution("guestLastName", payload.get('guest_last_name')))
        self.message.add_substitution(Substitution("hostFirstName", payload.get('host_first_name')))
        self.message.add_substitution(Substitution("guestFirstName", payload.get('guest_first_name')))
        self.message.add_substitution(Substitution("referenceNumber", payload.get('reference_number')))
        self.message.template_id = '0fff75c5-9f70-4959-a1e8-dc02066b8631'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            return response
        except Exception as e:
            raise e


    def cancelation_by_host_to_guest(self, payload):
        self.message.add_substitution(Substitution("hostLastName", payload.get('host_last_name')))
        self.message.add_substitution(Substitution("guestLastName", payload.get('guest_last_name')))
        self.message.add_substitution(Substitution("hostFirstName", payload.get('host_first_name')))
        self.message.add_substitution(Substitution("guestFirstName", payload.get('guest_first_name')))
        self.message.add_substitution(Substitution("referenceNumber", payload.get('reference_number')))

        self.message.template_id = 'b5f95ae4-e34a-473b-80b4-ee509495ef75'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            return response
        except Exception as e:
            raise e

    def cancelation_by_host_to_admin(self, payload):
        self.message.add_substitution(Substitution("hostLastName", payload.get('host_last_name')))
        self.message.add_substitution(Substitution("guestLastName", payload.get('guest_last_name')))
        self.message.add_substitution(Substitution("hostFirstName", payload.get('host_first_name')))
        self.message.add_substitution(Substitution("guestFirstName", payload.get('guest_first_name')))
        self.message.add_substitution(Substitution("referenceNumber", payload.get('reference_number')))

        self.message.template_id = '4d48e05e-052f-4066-92e6-9862e99984a6'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            return response
        except Exception as e:
            raise e


    def cancelation_by_guest_to_host(self, payload):
        self.message.add_substitution(Substitution("hostLastName", payload.get('host_last_name')))
        self.message.add_substitution(Substitution("guestLastName", payload.get('guest_last_name')))
        self.message.add_substitution(Substitution("hostFirstName", payload.get('host_first_name')))
        self.message.add_substitution(Substitution("guestFirstName", payload.get('guest_first_name')))
        self.message.add_substitution(Substitution("referenceNumber", payload.get('reference_number')))

        self.message.template_id = '89e7c9bc-c129-4a0d-8b98-e67033195158'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            return response
        except Exception as e:
            raise e


    def cancelation_by_guest_to_guest(self, payload):
        self.message.add_substitution(Substitution("hostLastName", payload.get('host_last_name')))
        self.message.add_substitution(Substitution("guestLastName", payload.get('guest_last_name')))
        self.message.add_substitution(Substitution("hostFirstName", payload.get('host_first_name')))
        self.message.add_substitution(Substitution("guestFirstName", payload.get('guest_first_name')))
        self.message.add_substitution(Substitution("referenceNumber", payload.get('reference_number')))

        self.message.template_id = '3feb41fb-4db4-404e-bd1d-3378c7a49788'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            return response
        except Exception as e:
            raise e

    def cancelation_by_guest_to_admin(self, payload):
        self.message.add_substitution(Substitution("hostLastName", payload.get('host_last_name')))
        self.message.add_substitution(Substitution("guestLastName", payload.get('guest_last_name')))
        self.message.add_substitution(Substitution("hostFirstName", payload.get('host_first_name')))
        self.message.add_substitution(Substitution("guestFirstName", payload.get('guest_first_name')))
        self.message.add_substitution(Substitution("referenceNumber", payload.get('reference_number')))

        self.message.template_id = 'b1c2d43a-695d-40e5-acbe-6e760ff757ac'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            return response
        except Exception as e:
            raise e



