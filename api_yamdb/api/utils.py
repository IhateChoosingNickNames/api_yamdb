from django.core import mail

from api_yamdb.settings import EMAIL_HOST

CODE_LENGTH = 10


def send_message(data, confirmation_code):
    email = mail.EmailMessage(
        subject="YaMDb",
        body=f"{confirmation_code}",
        from_email=EMAIL_HOST,
        to=[data["email"]],
    )
    email.send()
