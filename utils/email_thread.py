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

    def __init__(self, email_function):
        threading.Thread.__init__(self)
        self.email_function = email_function

    def run(self):
        # send_email(self.recipient, self.subject, self.message)
        # send_email_with_template()
        self.email_function()


class EmailService:
    message = None

    def __init__(self, recipient_email):
        self.message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=recipient_email,
            html_content='<strong>and easy to do anywhere, even with Python</strong>',
        )

        sender_name_sub = Substitution("Sender_Name", "Bongalo Ltd")
        self.message.add_substitution(sender_name_sub)

    def send_welcome(self, recipient_name):
        self.message.add_substitution(Substitution("name", recipient_name))

        self.message.template_id = '1c0076ca-2632-4457-b292-273cd87100ba'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            print("response from sendgrid ======>>>>>>")
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print("sendgrid error here below ====>>>>>>")
            print(e)

    def send_registration_pin(self, recipient_last_name, verification_pin):
        self.message.add_substitution(Substitution("lastName", recipient_last_name))
        self.message.add_substitution(Substitution('pinNumber', verification_pin))

        self.message.template_id = 'ff97b311-eb6c-4df7-b6a6-d11e2eb59dec'

        try:
            sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
            response = sendgrid_client.send(self.message)
            print("response from sendgrid ======>>>>>>")
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print("sendgrid error here below ====>>>>>>")
            print(e)



