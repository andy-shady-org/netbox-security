from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin
from dcim.models import Device, VirtualDeviceContext
from ipam.fields import IPNetworkField
from netbox.search import SearchIndex, register_search

from netbox_security.constants import ADDRESSLIST_ASSIGNMENT_MODELS
from netbox_security.models import SecurityZone


class AddressList(ContactsMixin, PrimaryModel):
    """
    """
    name = models.CharField(
        max_length=200
    )
    value = IPNetworkField(
        blank=True,
        null=True,
        help_text=_('An IP or Prefix in x.x.x.x/yy format')
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.SET_NULL,
        related_name="%(class)s_related",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = _('Address Lists')
        ordering = ('name', 'value')
        unique_together = ('name', 'value')

    def __str__(self):
        return f'{self.name}: {self.value}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_security:addresslist', args=[self.pk])


class AddressListAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to='contenttypes.ContentType',
        limit_choices_to=ADDRESSLIST_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField()
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type',
        fk_field='assigned_object_id'
    )
    address_list = models.ForeignKey(
        to='netbox_security.AddressList',
        on_delete=models.CASCADE
    )

    clone_fields = ('assigned_object_type', 'assigned_object_id')

    prerequisite_models = (
        'dcim.Device',
        'netbox_security.AddressList',
        'netbox_security.SecurityZone'
    )

    class Meta:
        indexes = (
            models.Index(fields=('assigned_object_type', 'assigned_object_id')),
        )
        constraints = (
            models.UniqueConstraint(
                fields=('assigned_object_type', 'assigned_object_id', 'address_list'),
                name='%(app_label)s_%(class)s_unique_device_address_list'
            ),
        )
        verbose_name = _('Address List Assignment')
        verbose_name_plural = _('Address List Assignments')

    def __str__(self):
        return f'{self.assigned_object}: {self.address_list}'

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class AddressListIndex(SearchIndex):
    model = AddressList
    fields = (
        ("name", 100),
        ("description", 500),
    )


GenericRelation(
    to=AddressListAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="device",
).contribute_to_class(Device, "address_lists")

GenericRelation(
    to=AddressListAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="security_zone",
).contribute_to_class(SecurityZone, "address_lists")

GenericRelation(
    to=AddressListAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="virtualdevicecontext",
).contribute_to_class(VirtualDeviceContext, "address_lists")
