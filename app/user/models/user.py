from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from user.managers import CustomUserManager
from utils.consts.user_role import CustomUserRoleChoices


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name=_('Email'))
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Name'))
    user_role = models.CharField(verbose_name=_('User Role'), max_length=15,
                                 choices=CustomUserRoleChoices.choices, default=CustomUserRoleChoices.USER.value)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['username']

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('User')

    def __str__(self):
        return f"{self.email}|{self.username}|{self.user_role}"
