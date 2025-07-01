from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from netbox.search import SearchIndex, register_search

from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin
from dcim.models import Device, VirtualDeviceContext, Interface

from netbox_security.constants import ZONE_ASSIGNMENT_MODELS


__all__ = ("SecurityZone", "SecurityZoneAssignment", "SecurityZoneIndex")


class SecurityZone(ContactsMixin, PrimaryModel):
    name = models.CharField(
        max_length=100,
    )
    identifier = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.SET_NULL,
        related_name="%(class)s_related",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = _("Security Zones")
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_security:securityzone", args=[self.pk])


class SecurityZoneAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=ZONE_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField(
        blank=True,
        null=True,
    )
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type",
        fk_field="assigned_object_id",
    )
    zone = models.ForeignKey(
        to="netbox_security.SecurityZone", on_delete=models.CASCADE
    )

    clone_fields = ("assigned_object_type", "assigned_object_id")

    prerequisite_models = ("netbox_security.SecurityZone",)

    class Meta:
        indexes = (models.Index(fields=("assigned_object_type", "assigned_object_id")),)
        constraints = (
            models.UniqueConstraint(
                fields=("assigned_object_type", "assigned_object_id", "zone"),
                name="%(app_label)s_%(class)s_unique_security_zone",
            ),
        )
        verbose_name = _("Security Zone assignment")
        verbose_name_plural = _("Security Zone assignments")

    def __str__(self):
        return f"{self.assigned_object}: {self.zone}"

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class SecurityZoneIndex(SearchIndex):
    model = SecurityZone
    fields = (
        ("name", 100),
        ("description", 500),
    )


GenericRelation(
    to=SecurityZoneAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="device",
).contribute_to_class(Device, "security_zones")

GenericRelation(
    to=SecurityZoneAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="virtualdevicecontext",
).contribute_to_class(VirtualDeviceContext, "security_zones")

GenericRelation(
    to=SecurityZoneAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="interface",
).contribute_to_class(Interface, "security_zones")
