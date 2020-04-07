import threading
from django.core.mail import send_mail
from django.conf import settings


def send_email(to, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to],
        fail_silently=False,
    )


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
        send_email(self.recipient, self.subject, self.message)