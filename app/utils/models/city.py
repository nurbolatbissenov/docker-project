from django.db import models
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    city = models.CharField(_("city"), max_length=255, unique=False)

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("City")

    def __str__(self):
        return self.city
