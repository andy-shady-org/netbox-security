from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin
from dcim.models import Device, VirtualDeviceContext
from netbox.search import SearchIndex, register_search

from netbox_security.constants import FILTER_ASSIGNMENT_MODELS
from netbox_security.choices import FamilyChoices


__all__ = (
    "FirewallFilter",
    "FirewallFilterAssignment",
    "FirewallFilterIndex",
)


class FirewallFilter(ContactsMixin, PrimaryModel):
    """ """

    name = models.CharField(max_length=200)
    family = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=FamilyChoices,
        default=FamilyChoices.INET,
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.SET_NULL,
        related_name="%(class)s_related",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = _("Firewall Filters")
        ordering = ("name", "family")
        unique_together = ("name", "family", "tenant")

    def __str__(self):
        return self.name

    def get_family_color(self):
        return FamilyChoices.colors.get(self.family)

    def get_absolute_url(self):
        return reverse("plugins:netbox_security:firewallfilter", args=[self.pk])


class FirewallFilterAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to="contenttypes.ContentType",
        limit_choices_to=FILTER_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField()
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type", fk_field="assigned_object_id"
    )
    firewall_filter = models.ForeignKey(
        to="netbox_security.FirewallFilter", on_delete=models.CASCADE
    )

    clone_fields = ("assigned_object_type", "assigned_object_id")

    prerequisite_models = ("netbox_security.FirewallFilter",)

    class Meta:
        indexes = (models.Index(fields=("assigned_object_type", "assigned_object_id")),)
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "assigned_object_type",
                    "assigned_object_id",
                    "firewall_filter",
                ),
                name="%(app_label)s_%(class)s_unique_firewall_filter",
            ),
        )
        verbose_name = _("Firewall Filter Assignment")
        verbose_name_plural = _("Firewall Filter Assignments")

    def __str__(self):
        return f"{self.assigned_object}: {self.firewall_filter}"

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class FirewallFilterIndex(SearchIndex):
    model = FirewallFilter
    fields = (
        ("name", 100),
        ("family", 300),
        ("description", 500),
    )


GenericRelation(
    to=FirewallFilterAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="device",
).contribute_to_class(Device, "firewall_filter")

GenericRelation(
    to=FirewallFilterAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="virtualdevicecontext",
).contribute_to_class(VirtualDeviceContext, "firewall_filter")
