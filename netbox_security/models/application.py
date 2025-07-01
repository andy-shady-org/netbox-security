from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin
from dcim.models import Device, VirtualDeviceContext
from netbox.search import SearchIndex, register_search

from netbox_security.fields import ChoiceArrayField
from netbox_security.choices import ProtocolChoices
from netbox_security.constants import APPLICATION_ASSIGNMENT_MODELS
from netbox_security.mixins import PortsMixin

__all__ = ("Application", "ApplicationAssignment", "ApplicationIndex")


class Application(ContactsMixin, PortsMixin, PrimaryModel):
    name = models.CharField(max_length=255)
    identifier = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    application_items = models.ManyToManyField(
        to="netbox_security.ApplicationItem",
        blank=True,
        related_name="+",
    )
    protocol = ChoiceArrayField(
        base_field=models.CharField(
            choices=ProtocolChoices,
            blank=True,
        ),
        null=True,
        blank=True,
        default=list,
        verbose_name=_("Protocols"),
        size=5,
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.SET_NULL,
        related_name="%(class)s_related",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = _("Applications")
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_security:application", args=[self.pk])

    @property
    def protocol_list(self):
        return ", ".join(self.protocol) if self.protocol else ""


class ApplicationAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to="contenttypes.ContentType",
        limit_choices_to=APPLICATION_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField()
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type", fk_field="assigned_object_id"
    )
    application = models.ForeignKey(
        to="netbox_security.Application", on_delete=models.CASCADE
    )
    clone_fields = ("assigned_object_type", "assigned_object_id")

    prerequisite_models = ("netbox_security.Application",)

    class Meta:
        indexes = (models.Index(fields=("assigned_object_type", "assigned_object_id")),)
        constraints = (
            models.UniqueConstraint(
                fields=("assigned_object_type", "assigned_object_id", "application"),
                name="%(app_label)s_%(class)s_unique_application",
            ),
        )
        verbose_name = _("Application assignment")
        verbose_name_plural = _("Application assignments")

    def __str__(self):
        return f"{self.assigned_object}: {self.application}"

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class ApplicationIndex(SearchIndex):
    model = Application
    fields = (
        ("name", 100),
        ("description", 500),
    )


GenericRelation(
    to=ApplicationAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="device",
).contribute_to_class(Device, "applications")

GenericRelation(
    to=ApplicationAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="virtualdevicecontext",
).contribute_to_class(VirtualDeviceContext, "applications")
