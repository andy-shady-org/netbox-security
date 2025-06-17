from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin
from dcim.models import Device, VirtualDeviceContext
from virtualization.models import VirtualMachine
from ipam.choices import IPAddressStatusChoices
from netbox.search import SearchIndex, register_search

from netbox_security.constants import (
    POOL_ASSIGNMENT_MODELS,
)

from netbox_security.choices import (
    PoolTypeChoices,
)

__all__ = (
    "NatPool",
    "NatPoolAssignment",
    "NatPoolIndex",
)


class NatPool(ContactsMixin, PrimaryModel):
    """ """

    name = models.CharField(max_length=100)
    pool_type = models.CharField(
        max_length=30, choices=PoolTypeChoices, default=PoolTypeChoices.ADDRESS
    )
    status = models.CharField(
        max_length=50,
        choices=IPAddressStatusChoices,
        default=IPAddressStatusChoices.STATUS_ACTIVE,
        verbose_name=_("Status"),
        help_text=_("The operational status of this NAT Pool"),
    )

    class Meta:
        verbose_name = _("NAT Pool")
        verbose_name_plural = _("NAT Pools")
        unique_together = ["name", "pool_type"]

    def __str__(self):
        return self.name

    def get_status_color(self):
        return IPAddressStatusChoices.colors.get(self.status)

    def get_absolute_url(self):
        return reverse("plugins:netbox_security:natpool", args=[self.pk])


class NatPoolAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to="contenttypes.ContentType",
        limit_choices_to=POOL_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField()
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type", fk_field="assigned_object_id"
    )
    pool = models.ForeignKey(to="netbox_security.NatPool", on_delete=models.CASCADE)

    clone_fields = ("assigned_object_type", "assigned_object_id")

    prerequisite_models = ("netbox_security.NatPool",)

    class Meta:
        indexes = (models.Index(fields=("assigned_object_type", "assigned_object_id")),)
        constraints = (
            models.UniqueConstraint(
                fields=("assigned_object_type", "assigned_object_id", "pool"),
                name="%(app_label)s_%(class)s_unique_nat_pool",
            ),
        )
        verbose_name = _("NAT Pool assignment")
        verbose_name_plural = _("NAT Pool assignments")

    def __str__(self):
        return f"{self.assigned_object}: {self.pool}"

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class NatPoolIndex(SearchIndex):
    model = NatPool
    fields = (
        ("name", 100),
        ("pool_type", 300),
        ("status", 300),
    )


GenericRelation(
    to=NatPoolAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="device",
).contribute_to_class(Device, "nat_pools")

GenericRelation(
    to=NatPoolAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="virtualdevicecontext",
).contribute_to_class(VirtualDeviceContext, "nat_pools")

GenericRelation(
    to=NatPoolAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="virtualmachine",
).contribute_to_class(VirtualMachine, "nat_pools")
