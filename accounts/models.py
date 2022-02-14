from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


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
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    activity = models.CharField('Активность', max_length=100, blank=True, null=True)
    nickname = models.CharField('Прозвище', max_length=50, blank=True, null=True)
    # task = models.ForeignKey('tasker.Task', blank=True, null=True, on_delete=models.CASCADE, related_name='Задачи')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'nickname', 'activity', 'full_name']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


# class Profile(models.Model):
#     """Модель профиль пользователя"""
#     user_info = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, name='userInfo')
#     task = models.ForeignKey('tasker.Task', blank=True, null=True, on_delete=models.CASCADE, related_name='Задачи')
#
#
#     def __str__(self):
#         return self.user.first_name
#
#     class Meta:
#         verbose_name = 'Профиль'
#         verbose_name_plural = 'Профиль'