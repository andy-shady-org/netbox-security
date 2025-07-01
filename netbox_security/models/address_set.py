from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin
from dcim.models import Device, VirtualDeviceContext
from netbox.search import SearchIndex, register_search

from netbox_security.constants import ADDRESS_ASSIGNMENT_MODELS
from netbox_security.models import SecurityZone


__all__ = ("AddressSet", "AddressSetAssignment", "AddressSetIndex")


class AddressSet(ContactsMixin, PrimaryModel):
    """ """

    name = models.CharField(max_length=200)
    identifier = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    addresses = models.ManyToManyField(
        to="netbox_security.Address",
        related_name="%(class)s_addresses",
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.SET_NULL,
        related_name="%(class)s_related",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = _("Address Sets")
        ordering = ("name",)
        unique_together = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_security:addressset", args=[self.pk])


class AddressSetAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to="contenttypes.ContentType",
        limit_choices_to=ADDRESS_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField()
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type", fk_field="assigned_object_id"
    )
    address_set = models.ForeignKey(
        to="netbox_security.AddressSet", on_delete=models.CASCADE
    )

    clone_fields = ("assigned_object_type", "assigned_object_id")

    prerequisite_models = ("netbox_security.AddressSet",)

    class Meta:
        indexes = (models.Index(fields=("assigned_object_type", "assigned_object_id")),)
        constraints = (
            models.UniqueConstraint(
                fields=("assigned_object_type", "assigned_object_id", "address_set"),
                name="%(app_label)s_%(class)s_unique_address",
            ),
        )
        verbose_name = _("Address Set Assignment")
        verbose_name_plural = _("Address Set Assignments")

    def __str__(self):
        return f"{self.assigned_object}: {self.address_set}"

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class AddressSetIndex(SearchIndex):
    model = AddressSet
    fields = (
        ("name", 100),
        ("description", 500),
    )


GenericRelation(
    to=AddressSetAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="device",
).contribute_to_class(Device, "address_sets")

GenericRelation(
    to=AddressSetAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="security_zone",
).contribute_to_class(SecurityZone, "address_sets")

GenericRelation(
    to=AddressSetAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="virtualdevicecontext",
).contribute_to_class(VirtualDeviceContext, "address_sets")
