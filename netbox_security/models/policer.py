from django.urls import reverse
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from netbox.search import SearchIndex, register_search

from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin
from dcim.models import Device, VirtualDeviceContext

from netbox_security.constants import (
    POLICER_ASSIGNMENT_MODELS,
)

from netbox_security.choices import ForwardingClassChoices, LossPriorityChoices


__all__ = (
    "Policer",
    "PolicerAssignment",
    "PolicerIndex",
)


class Policer(ContactsMixin, PrimaryModel):
    name = models.CharField(
        max_length=100,
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.SET_NULL,
        related_name="%(class)s_related",
        blank=True,
        null=True,
    )
    logical_interface_policer = models.BooleanField(
        blank=True, null=True, help_text=_("Policer is logical interface policer")
    )
    physical_interface_policer = models.BooleanField(
        blank=True, null=True, help_text=_("Policer is physical interface policer")
    )
    bandwidth_limit = models.PositiveIntegerField(
        validators=[
            MinValueValidator(32000),
            MaxValueValidator(50000000000),
        ],
        blank=True,
        null=True,
        help_text=_("Bandwidth limit (32000..50000000000 bits per second)"),
    )
    bandwidth_percent = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
        blank=True,
        null=True,
        help_text=_("Bandwidth limit in percentage (1..100 percent)"),
    )
    burst_size_limit = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1500),
            MaxValueValidator(100000000000),
        ],
        blank=True,
        null=True,
        help_text=_("Burst size limit (1500..100000000000 bytes)"),
    )
    discard = models.BooleanField(
        blank=True, null=True, help_text=_("Discard the packet")
    )
    out_of_profile = models.BooleanField(
        blank=True,
        null=True,
        help_text=_("Discard packets only if both congested and over threshold"),
    )
    loss_priority = models.CharField(
        choices=LossPriorityChoices,
        blank=True,
        null=True,
        help_text=_("Packet's loss priority"),
    )
    forwarding_class = models.CharField(
        choices=ForwardingClassChoices,
        blank=True,
        null=True,
        help_text=_("Classify packet to forwarding class"),
    )

    class Meta:
        verbose_name_plural = _("Policers")
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_security:policer", args=[self.pk])

    def get_loss_priority_color(self):
        return LossPriorityChoices.colors.get(self.loss_priority)

    def get_forwarding_class_color(self):
        return ForwardingClassChoices.colors.get(self.forwarding_class)


class PolicerAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=POLICER_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField()

    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type",
        fk_field="assigned_object_id",
    )
    policer = models.ForeignKey(to="netbox_security.Policer", on_delete=models.CASCADE)

    clone_fields = ("assigned_object_type", "assigned_object_id")

    prerequisite_models = ("netbox_security.Policer",)

    class Meta:
        indexes = (models.Index(fields=("assigned_object_type", "assigned_object_id")),)
        constraints = (
            models.UniqueConstraint(
                fields=("assigned_object_type", "assigned_object_id", "policer"),
                name="%(app_label)s_%(class)s_unique_policer",
            ),
        )
        verbose_name = _("Policer assignment")
        verbose_name_plural = _("Policer assignments")

    def __str__(self):
        return f"{self.assigned_object}: {self.policer}"

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class PolicerIndex(SearchIndex):
    model = Policer
    fields = (
        ("name", 100),
        ("description", 500),
    )


GenericRelation(
    to=PolicerAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="device",
).contribute_to_class(Device, "policers")

GenericRelation(
    to=PolicerAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="virtualdevicecontext",
).contribute_to_class(VirtualDeviceContext, "policers")
