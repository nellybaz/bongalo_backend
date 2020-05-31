import threading
from django.core.mail import send_mail
from django.conf import settings

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Personalization, Email, Substitution




def send_email(to, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to],
        fail_silently=False,
    )


def send_email_with_template():
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails='nellybaz10@gmail.com',
        html_content='<strong>and easy to do anywhere, even with Python</strong>',
    )

    # p = Personalization()
    # p.dynamic_template_data = {
    #     'name': 'Nelson',
    # }
    # message.add_personalization(p)

    sub = Substitution("name", "Nelson")
    message.add_substitution(sub)

    message.template_id = '1c0076ca-2632-4457-b292-273cd87100ba'

    try:
        print('sendgrid api key is {0}'.format(settings.SENDGRID_API_KEY))
        sendgrid_client = SendGridAPIClient(os.environ.get(settings.SENDGRID_API_KEY))
        response = sendgrid_client.send(message)
        print("response from sendgrid ======>>>>>>")
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("sendgrid error here below ====>>>>>>")
        print(e)


class SendEmailThread(threading.Thread):
    message = None
    recipient = None
    subject = None

    def __init__(self, recipient, subject, message):
        threading.Thread.__init__(self)
        self.recipient = recipient
        self.subject = subject
        self.message = message

    def run(self):
        # send_email(self.recipient, self.subject, self.message)
        send_email_with_template()
