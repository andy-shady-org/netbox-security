from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from netbox.models import PrimaryModel
from netbox.models.features import ContactsMixin
from netbox.search import SearchIndex, register_search

from netbox_security.fields import ChoiceArrayField
from netbox_security.choices import ProtocolChoices
from netbox_security.mixins import PortsMixin

__all__ = ("ApplicationItem", "ApplicationItemIndex")


class ApplicationItem(ContactsMixin, PortsMixin, PrimaryModel):
    name = models.CharField(max_length=255)
    index = models.PositiveIntegerField()
    protocol = ChoiceArrayField(
        base_field=models.CharField(
            choices=ProtocolChoices,
            blank=True,
        ),
        default=list,
        verbose_name=_("Protocols"),
        null=True,
        blank=True,
        size=5,
    )

    class Meta:
        verbose_name_plural = _("Application Items")
        ordering = ["index", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_security:applicationitem", args=[self.pk])

    @property
    def protocol_list(self):
        return ", ".join(self.protocol) if self.protocol else ""


@register_search
class ApplicationItemIndex(SearchIndex):
    model = ApplicationItem
    fields = (
        ("name", 100),
        ("description", 500),
    )
