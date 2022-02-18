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
    activity = models.CharField('Активность', max_length=100, blank=True, null=True)
    nickname = models.CharField('Прозвище', max_length=50, blank=True, null=True)
    favorite_ids = models.ManyToManyField('tasker.Task', blank=True, null=True, name='favoriteIds')
    joined_date = models.DateTimeField(auto_now_add=True, name='joinedDate')
    picture = models.CharField(max_length=255)
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    # task = models.ForeignKey('tasker.Task', blank=True, null=True, on_delete=models.CASCADE, related_name='Задачи')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'nickname', 'activity', 'fullname']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email