from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import CustomUser
from utils.models import City


class Address(models.Model):
    district = models.CharField(_("district"), max_length=255, unique=False)
    house = models.CharField(_("house"), max_length=255, unique=False)
    apartment = models.CharField(_("apartment"), max_length=255, unique=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Address")
        verbose_name_plural = ("Address")

    def __str__(self):
        return f'{self.district}-{self.house}-{self.apartment}'
