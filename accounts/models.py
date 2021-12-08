from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

ROLES = (
    ('User', 'User'),
    ('Admin', 'Admin'),
    ('Editor', 'Editor'),
)

class UserAccountManager(BaseUserManager):
    def create_user(self, email, login, password=None, **extra_fields):
        if not login:
            raise ValueError('Указанное имя пользователя должно быть установлено')

        if not email:
            raise ValueError('Данный адрес электронной почты должен быть установлен')

        email = self.normalize_email(email)
        user = self.model(email=email, login=login, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, login, password):
        user = self.create_user(email, login, password)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    """Пользовательская модель User"""
    login = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    roles = models.CharField(max_length=50, choices=ROLES, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    #call_sign(name=callSign)
    activity = models.CharField(max_length=100, null=True, blank=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.login

    def get_short_name(self):
        return self.login

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'



