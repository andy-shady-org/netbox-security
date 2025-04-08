from django.urls import reverse
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from netbox.search import SearchIndex, register_search

from netbox.models import PrimaryModel
from netbox.models.features import ContactsMixin
from netbox_security.choices import ActionChoices


__all__ = (
    "SecurityZonePolicy",
    "SecurityZonePolicyIndex",
)


class SecurityZonePolicy(ContactsMixin, PrimaryModel):
    name = models.CharField(
        max_length=100,
    )
    index = models.PositiveIntegerField()
    source_zone = models.ForeignKey(
        to="netbox_security.SecurityZone",
        related_name="source_zone_policies",
        on_delete=models.CASCADE,
    )
    destination_zone = models.ForeignKey(
        to="netbox_security.SecurityZone",
        related_name="destination_zone_policies",
        on_delete=models.CASCADE,
    )
    source_address = models.ManyToManyField(
        to="netbox_security.AddressList",
        related_name="%(class)s_source_address",
    )
    destination_address = models.ManyToManyField(
        to="netbox_security.AddressList",
        related_name="%(class)s_destination_address",
    )
    application = ArrayField(
        models.CharField(
            max_length=50,
            blank=True,
            null=True,
        ),
        size=20,
        verbose_name=_("Applications"),
        blank=True,
        null=True,
    )
    actions = ArrayField(
        models.CharField(
            max_length=20,
            blank=True,
            null=True,
            choices=ActionChoices,
            default=ActionChoices.PERMIT,
        ),
        size=4,
        verbose_name=_("Actions"),
    )
    prerequisite_models = (
        "netbox_security.SecurityZone",
        "netbox_security.AddressList",
    )

    class Meta:
        verbose_name_plural = _("Security Zone Policies")
        ordering = ["index", "name"]
        unique_together = ["name", "source_zone", "destination_zone"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_security:securityzonepolicy", args=[self.pk])


@register_search
class SecurityZonePolicyIndex(SearchIndex):
    model = SecurityZonePolicy
    fields = (
        ("name", 100),
        ("description", 500),
    )
