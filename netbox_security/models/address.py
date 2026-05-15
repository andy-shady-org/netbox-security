from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.exceptions import ValidationError
from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin
from ipam.models import IPAddress, Prefix, IPRange
from dcim.models import Device, VirtualDeviceContext
from virtualization.models import VirtualMachine
from netbox.search import SearchIndex, register_search

from netbox_security.constants import (
    ADDRESS_ASSIGNMENT_MODELS,
    ADDRESS_FIELD_ASSIGNMENT_MODELS,
)
from netbox_security.models import SecurityZone, CustomPrefix
from netbox_security.validators import validate_fqdn

__all__ = ("Address", "AddressAssignment", "AddressIndex")


class Address(ContactsMixin, PrimaryModel):
    """ """

    name = models.CharField(max_length=200)
    identifier = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    assigned_object_type = models.ForeignKey(
        to="contenttypes.ContentType",
        limit_choices_to=ADDRESS_FIELD_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="+",
    )
    assigned_object_id = models.PositiveBigIntegerField(null=True, blank=True)
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type", fk_field="assigned_object_id"
    )
    dns_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Fully qualified hostname (wildcard allowed)"),
        validators=[validate_fqdn],
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.SET_NULL,
        related_name="%(class)s_related",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = _("Addresses")
        ordering = ("name",)
        unique_together = [
            "name",
            "identifier",
        ]
        constraints = [
            models.CheckConstraint(
                condition=(
                    # Choice 1: GFK is defined, DNS is totally empty (NULL or "")
                    models.Q(assigned_object_id__isnull=False, dns_name__isnull=True)
                    | models.Q(assigned_object_id__isnull=False, dns_name="")
                    |
                    # Choice 2: GFK is null, DNS contains actual string values
                    models.Q(assigned_object_id__isnull=True, dns_name__isnull=False)
                    & ~models.Q(dns_name="")
                ),
                name="exclusive_assigned_object_or_dns_name",
            )
        ]

    def __str__(self):
        if self.dns_name:
            return f"{self.name}: {self.dns_name}"
        else:
            return f"{self.name}: {self.assigned_object}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_security:address", args=[self.pk])

    def clean(self):
        super().clean()
        has_gfk = bool(self.assigned_object_id)
        has_dns = bool(self.dns_name)

        # 1. Enforce that at least one field must be filled
        if not has_gfk and not has_dns:
            raise ValidationError("Requires either an assigned object or a dns name.")

        # 2. Enforce mutual exclusivity (cannot have both)
        if has_gfk and has_dns:
            raise ValidationError(
                "Cannot define both an assigned object and a dns name at the same time."
            )


class AddressAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to="contenttypes.ContentType",
        limit_choices_to=ADDRESS_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField()
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type", fk_field="assigned_object_id"
    )
    address = models.ForeignKey(to="netbox_security.Address", on_delete=models.CASCADE)

    clone_fields = ("assigned_object_type", "assigned_object_id")

    prerequisite_models = ("netbox_security.Address",)

    class Meta:
        indexes = (models.Index(fields=("assigned_object_type", "assigned_object_id")),)
        constraints = (
            models.UniqueConstraint(
                fields=("assigned_object_type", "assigned_object_id", "address"),
                name="%(app_label)s_%(class)s_unique_address",
            ),
        )
        ordering = ("address", "assigned_object_id")
        verbose_name = _("Address Assignment")
        verbose_name_plural = _("Address Assignments")

    def __str__(self):
        return f"{self.assigned_object}: {self.address}"

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class AddressIndex(SearchIndex):
    model = Address
    fields = (
        ("name", 100),
        ("dns_name", 100),
        ("identifier", 300),
        ("description", 500),
    )


GenericRelation(
    to=Address,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="custom_prefixes",
).contribute_to_class(CustomPrefix, "addresses")

GenericRelation(
    to=Address,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="prefixes",
).contribute_to_class(Prefix, "addresses")

GenericRelation(
    to=Address,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="ip_addresses",
).contribute_to_class(IPAddress, "addresses")

GenericRelation(
    to=Address,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="ip_ranges",
).contribute_to_class(IPRange, "addresses")

GenericRelation(
    to=AddressAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="device",
).contribute_to_class(Device, "addresses")

GenericRelation(
    to=AddressAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="security_zone",
).contribute_to_class(SecurityZone, "addresses")

GenericRelation(
    to=AddressAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="virtualdevicecontext",
).contribute_to_class(VirtualDeviceContext, "addresses")

GenericRelation(
    to=AddressAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="virtualmachine",
).contribute_to_class(VirtualMachine, "addresses")
