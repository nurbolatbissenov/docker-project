from django.db import models


class CustomUserRoleChoices(models.TextChoices):
    ADMIN = 'admin', 'Админ'
    MANAGER = 'manager', 'Менеджер'
    USER = 'user', 'Пользователь'