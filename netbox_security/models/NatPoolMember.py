from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from netbox.search import SearchIndex, register_search

from netbox.models import NetBoxModel
from utilities.data import array_to_string
from ipam.constants import *
from ipam.choices import IPAddressStatusChoices


__all__ = (
    'NatPoolMember',
    'NatPoolMemberIndex',
)


class NatPoolMember(NetBoxModel):
    """
    """
    name = models.CharField(
        max_length=100
    )
    pool = models.ForeignKey(
        to='netbox_security.NatPool',
        on_delete=models.CASCADE,
        related_name="%(class)s_pools"
    )
    status = models.CharField(
        max_length=50,
        choices=IPAddressStatusChoices,
        default=IPAddressStatusChoices.STATUS_ACTIVE,
        verbose_name=_('Status'),
        help_text=_('The operational status of this NAT Pool Member')
    )
    address = models.ForeignKey(
        to='ipam.IPAddress',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    prefix = models.ForeignKey(
        to='ipam.Prefix',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    address_range = models.ForeignKey(
        to='ipam.IPRange',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    source_ports = ArrayField(
        base_field=models.PositiveIntegerField(
            validators=[
                MinValueValidator(SERVICE_PORT_MIN),
                MaxValueValidator(SERVICE_PORT_MAX)
            ]
        ),
        null=True,
        verbose_name=_('Source Port numbers')
    )
    destination_ports = ArrayField(
        base_field=models.PositiveIntegerField(
            validators=[
                MinValueValidator(SERVICE_PORT_MIN),
                MaxValueValidator(SERVICE_PORT_MAX)
            ]
        ),
        null=True,
        verbose_name=_('Destination Port numbers')
    )
    prerequisite_models = (
        'netbox_security.NatPool',
    )

    class Meta:
        verbose_name = _('NAT Pool Member')
        verbose_name_plural = _('NAT Pool Members')
        ordering = ('pool', 'name')
        unique_together = ('pool', 'name')

    @property
    def network(self):
        return self.prefix

    def __str__(self):
        return f'{self.name}'

    @property
    def source_port_list(self):
        return array_to_string(self.source_ports)

    @property
    def destination_port_list(self):
        return array_to_string(self.destination_ports)

    def get_status_color(self):
        return IPAddressStatusChoices.colors.get(self.status)

    def get_absolute_url(self):
        return reverse('plugins:netbox_security:natpoolmember', args=[self.pk])

    def clean(self):
        super().clean()
        # make sure that only one field is set
        if self.prefix and self.address and self.address_range:
            raise ValidationError(
                    {'prefix': 'Cannot set Address, Prefix and Address Range fields'}
                )

        if self.address and self.address_range:
            raise ValidationError(
                    {'prefix': 'Cannot set Address and Address Range fields'}
                )

        if self.prefix and self.address_range:
            raise ValidationError(
                    {'prefix': 'Cannot set Prefix and Address Range fields'}
                )

        if self.prefix and self.address:
            raise ValidationError(
                    {'prefix': 'Cannot set Address and Prefix fields'}
                )

        # at least one field must be set
        if self.prefix is None and self.address is None and self.address_range is None:
            raise ValidationError(
                    {'prefix': 'Cannot set all fields to Null'}
                )


@register_search
class NatPoolMemberIndex(SearchIndex):
    model = NatPoolMember
    fields = (
        ("name", 100),
        ("pool", 300),
        ("address", 300),
        ("prefix", 300),
        ("address_range", 300),
        ("status", 300),
    )