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

    def send_payment_confirmation(self, payload):
        self.message.add_substitution(Substitution("lastName", payload['lastName']))
        self.message.add_substitution(Substitution('nameOfPlace', payload['nameOfPlace']))
        self.message.add_substitution(Substitution('nameOfHost', payload['nameOfHost']))
        self.message.add_substitution(Substitution('dateOfPayment', payload['dateOfPayment']))
        self.message.add_substitution(Substitution('bookingReference', payload['bookingReference']))

        self.message.add_substitution(Substitution('name', payload['name']))
        self.message.add_substitution(Substitution('dateFrom', payload['dateFrom']))
        self.message.add_substitution(Substitution('dateTo', payload['dateTo']))
        self.message.add_substitution(Substitution('checkinTime', payload['checkinTime']))
        self.message.add_substitution(Substitution('checkoutTime', payload['checkoutTime']))

        self.message.add_substitution(Substitution('appartmentName', payload['appartmentName']))
        self.message.add_substitution(Substitution('price', payload['price']))
        self.message.add_substitution(Substitution('numberOfNight', payload['numberOfNight']))
        self.message.add_substitution(Substitution('serviceFee', payload['serviceFee']))

        self.message.add_substitution(Substitution('total', payload['total']))


        self.message.template_id = '7e8da248-c9c0-4a7a-84b0-0e805c7f5fe6'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            return response
        except Exception as e:
            print("sendgrid error here below ====>>>>>>")
            print(e)
            raise e



