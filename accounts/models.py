from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, name='firstName')
    last_name = models.CharField(max_length=255, name='lastName')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

#from django.conf import settings
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
#
# ROLES = (
#     ('User', 'User'),
#     ('Admin', 'Admin'),
#     ('Editor', 'Editor'),
# )
#
#
# class UserAccountManager(BaseUserManager):
#     def create_user(self, email, login, password=None, **extra_fields):
#         if not login:
#             raise ValueError('Указанное имя пользователя должно быть установлено')
#
#         if not email:
#             raise ValueError('Данный адрес электронной почты должен быть установлен')
#
#         email = self.normalize_email(email)
#         user = self.model(email=email, login=login, **extra_fields)
#
#         user.set_password(password)
#         user.save()
#
#         return user
#
#     def create_superuser(self, email, login, password):
#         user = self.create_user(email, login, password)
#
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()
#
#         return user
#
#
# class UserAccount(AbstractBaseUser, PermissionsMixin):
#     """Пользовательская модель User"""
#     login = models.CharField(max_length=255, unique=True)
#     email = models.EmailField(max_length=255, unique=True)
#     roles = models.CharField(max_length=50, choices=ROLES, null=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     #call_sign(name=callSign)
#     activity = models.CharField(max_length=100, null=True, blank=True)
#
#     objects = UserAccountManager()
#
#     USERNAME_FIELD = 'login'
#     REQUIRED_FIELDS = ['email']
#
#     def get_full_name(self):
#         return self.login
#
#     def get_short_name(self):
#         return self.login
#
#     def __str__(self):
#         return self.email
#
#     class Meta:
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователь'
#
#
#
