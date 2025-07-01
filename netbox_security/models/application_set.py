from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin
from dcim.models import Device, VirtualDeviceContext
from netbox.search import SearchIndex, register_search

from netbox_security.constants import APPLICATION_ASSIGNMENT_MODELS


__all__ = ("ApplicationSet", "ApplicationSetAssignment", "ApplicationSetIndex")


class ApplicationSet(ContactsMixin, PrimaryModel):
    """ """

    name = models.CharField(max_length=200)
    identifier = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    applications = models.ManyToManyField(
        to="netbox_security.Application",
        related_name="+",
        blank=True,
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.SET_NULL,
        related_name="%(class)s_related",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = _("Application Sets")
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_security:applicationset", args=[self.pk])


class ApplicationSetAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to="contenttypes.ContentType",
        limit_choices_to=APPLICATION_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField()
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type", fk_field="assigned_object_id"
    )
    application_set = models.ForeignKey(
        to="netbox_security.ApplicationSet", on_delete=models.CASCADE
    )

    clone_fields = ("assigned_object_type", "assigned_object_id")

    prerequisite_models = ("netbox_security.ApplicationSet",)

    class Meta:
        indexes = (models.Index(fields=("assigned_object_type", "assigned_object_id")),)
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "assigned_object_type",
                    "assigned_object_id",
                    "application_set",
                ),
                name="%(app_label)s_%(class)s_unique_address",
            ),
        )
        verbose_name = _("Application Set Assignment")
        verbose_name_plural = _("Application Set Assignments")

    def __str__(self):
        return f"{self.assigned_object}: {self.application_set}"

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class ApplicationSetIndex(SearchIndex):
    model = ApplicationSet
    fields = (
        ("name", 100),
        ("description", 500),
    )


GenericRelation(
    to=ApplicationSetAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="device",
).contribute_to_class(Device, "application_sets")

GenericRelation(
    to=ApplicationSetAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="virtualdevicecontext",
).contribute_to_class(VirtualDeviceContext, "application_sets")
