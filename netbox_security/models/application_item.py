from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from netbox.models import PrimaryModel
from netbox.models.features import ContactsMixin
from ipam.constants import SERVICE_PORT_MIN, SERVICE_PORT_MAX
from netbox.search import SearchIndex, register_search

from netbox_security.choices import ProtocolChoices

__all__ = ("ApplicationItem", "ApplicationItemIndex")


class ApplicationItem(ContactsMixin, PrimaryModel):
    name = models.CharField(max_length=255)
    index = models.PositiveIntegerField()
    protocol = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        choices=ProtocolChoices,
        default=ProtocolChoices.TCP,
    )
    destination_port = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(SERVICE_PORT_MIN),
            MaxValueValidator(SERVICE_PORT_MAX),
        ],
    )
    source_port = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(SERVICE_PORT_MIN),
            MaxValueValidator(SERVICE_PORT_MAX),
        ],
    )

    class Meta:
        verbose_name_plural = _("Application Items")
        ordering = ["index", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_security:applicationitem", args=[self.pk])


@register_search
class ApplicationItemIndex(SearchIndex):
    model = ApplicationItem
    fields = (
        ("name", 100),
        ("description", 500),
    )
