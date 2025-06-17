from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from netbox.search import SearchIndex, register_search

from netbox.models import NetBoxModel, PrimaryModel
from netbox.models.features import ContactsMixin

from dcim.models import Device, VirtualDeviceContext
from virtualization.models import VirtualMachine

from netbox_security.constants import (
    RULESET_ASSIGNMENT_MODELS,
)

from netbox_security.choices import (
    RuleDirectionChoices,
    NatTypeChoices,
)


__all__ = (
    "NatRuleSet",
    "NatRuleSetAssignment",
    "NatRuleSetIndex",
)


class NatRuleSet(ContactsMixin, PrimaryModel):
    """ """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    nat_type = models.CharField(
        max_length=30, choices=NatTypeChoices, default=NatTypeChoices.TYPE_STATIC
    )
    source_zones = models.ManyToManyField(
        to="netbox_security.SecurityZone",
        blank=True,
        related_name="%(class)s_source_zones",
    )
    destination_zones = models.ManyToManyField(
        to="netbox_security.SecurityZone",
        blank=True,
        related_name="%(class)s_destination_zones",
    )
    direction = models.CharField(
        max_length=30,
        choices=RuleDirectionChoices,
        default=RuleDirectionChoices.DIRECTION_INBOUND,
    )
    prerequisite_models = ("dcim.Device",)

    class Meta:
        verbose_name_plural = "NAT Rule Sets"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_security:natruleset", args=[self.pk])


class NatRuleSetAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=RULESET_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField()

    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type",
        fk_field="assigned_object_id",
    )
    ruleset = models.ForeignKey(
        to="netbox_security.NatRuleSet", on_delete=models.CASCADE
    )

    clone_fields = ("assigned_object_type", "assigned_object_id")

    prerequisite_models = ("dcim.Device",)

    class Meta:
        indexes = (models.Index(fields=("assigned_object_type", "assigned_object_id")),)
        constraints = (
            models.UniqueConstraint(
                fields=("assigned_object_type", "assigned_object_id", "ruleset"),
                name="%(app_label)s_%(class)s_unique_nat_rule_set",
            ),
        )
        verbose_name = _("NAT Pool assignment")
        verbose_name_plural = _("NAT Ruleset assignments")

    def __str__(self):
        return f"{self.assigned_object}: {self.ruleset}"

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class NatRuleSetIndex(SearchIndex):
    model = NatRuleSet
    fields = (
        ("name", 100),
        ("nat_type", 300),
        ("source_zones", 300),
        ("destination_zones", 300),
        ("direction", 300),
    )


GenericRelation(
    to=NatRuleSetAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="device",
).contribute_to_class(Device, "natrulesets")

GenericRelation(
    to=NatRuleSetAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="virtualdevicecontext",
).contribute_to_class(VirtualDeviceContext, "natrulesets")

GenericRelation(
    to=NatRuleSetAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="virtualmachine",
).contribute_to_class(VirtualMachine, "natrulesets")
