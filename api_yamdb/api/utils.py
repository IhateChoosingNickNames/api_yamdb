import random

from django.core import mail

CODE_LENGTH = 10


def send_message(data, confirmation_code):
    email = mail.EmailMessage(
        subject="YaMDb",
        body=f"{confirmation_code}",
        from_email="site-owner@email.world",
        to=[data["email"]],
    )
    email.send()


def generate_code():
    """Генерация случайного кода."""
    tmp = [str(i) for i in range(CODE_LENGTH)]
    random.shuffle(tmp)
    return "".join(tmp)
