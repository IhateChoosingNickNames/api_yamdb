from rest_framework.exceptions import ValidationError


def additional_username_validator(value):
    if value == 'me':
        raise ValidationError('Такое имя пользователя недопустимо.')