from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


from .validators import additional_username_validator

ROLE_CHOICES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]



class UserManager(BaseUserManager):
    """Кастомный менеджер объектов модели User."""

    def create_user(self, email, username, role="user", password=None, **others):
        if not email:
            raise ValueError('У пользователя должен быть указан email')
        if username == 'me':
            raise ValueError('Такое имя пользователя недопустимо.')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role,
            **others
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **others):
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователей."""

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('Юзернейм'),
        max_length=150,
        unique=True,
        help_text=_('Обязательное поле. Не более 150 символов. Допустимые символы: буквы, цифры и @/./+/-/_.'),
        validators=[username_validator, additional_username_validator],
        error_messages={
            'unique': _("Пользователь с таким имененем уже существует."),
        },
    )
    email = models.EmailField(
        _('Почта'),
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        _('Имя'),
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        _('Фамилия'),
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        _('Биография'),
        blank=True,
        help_text="Опишите биографию пользователя."
    )
    role = models.TextField(
        _('Статус пользователя'),
        choices=ROLE_CHOICES,
        default="user",
        help_text=("Выберите статус пользователя. Дефолт - user. "
                   "От выбора зависят его права.")
    )
    is_active = models.BooleanField(
        _('Активный/неактивный.'),
        default=False,
        help_text=_('Статус текущего аккаунта - активирован или нет.'),
    )
    is_staff = models.BooleanField(
        default=False,
        help_text=_('Является ли пользователь суперюзером.'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    objects = UserManager()

class Auth(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name=_("Пользователь"),
        help_text=_("Инстанс связанного юзера."),
        on_delete=models.CASCADE,
        unique=True
    )
    confirmation_code = models.CharField(
        max_length=128,
        verbose_name=_("Код подтверждения"),
        help_text=_("Код подтверждения с почты."),
    )