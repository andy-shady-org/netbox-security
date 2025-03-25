from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from netbox.search import SearchIndex, register_search

from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin

from utilities.data import array_to_string

from ipam.constants import *
from dcim.models import Interface

from netbox_security.constants.constants import (
    RULE_ASSIGNMENT_MODELS
)

from netbox_security.choices import (
    RuleStatusChoices,
    CustomInterfaceChoices,
    AddressTypeChoices,
)


__all__ = (
    'NatRule',
    'NatRuleAssignment',
    'NatRuleIndex',
)


class NatRule(ContactsMixin, PrimaryModel):
    """
    """
    rule_set = models.ForeignKey(
        to='netbox_security.NatRuleSet',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="%(class)s_rules"
    )
    pool = models.ForeignKey(
        to='netbox_security.NatPool',
        on_delete=models.PROTECT,
        null=True,
    )
    name = models.CharField(
        max_length=100
    )
    status = models.CharField(
        max_length=50,
        choices=RuleStatusChoices,
        default=RuleStatusChoices.STATUS_ACTIVE
    )
    source_type = models.CharField(
        max_length=50,
        choices=AddressTypeChoices,
        default=AddressTypeChoices.STATIC
    )
    destination_type = models.CharField(
        max_length=50,
        choices=AddressTypeChoices,
        default=AddressTypeChoices.STATIC
    )
    source_addresses = models.ManyToManyField(
        to='ipam.IPAddress',
        blank=True,
        related_name="%(class)s_source_addresses"
    )
    destination_addresses = models.ManyToManyField(
        to='ipam.IPAddress',
        blank=True,
        related_name="%(class)s_destination_addresses"
    )
    source_prefixes = models.ManyToManyField(
        to='ipam.Prefix',
        blank=True,
        related_name="%(class)s_source_prefixes",
    )
    destination_prefixes = models.ManyToManyField(
        to='ipam.Prefix',
        blank=True,
        related_name="%(class)s_destination_prefixes",
    )
    source_ranges = models.ManyToManyField(
        to='ipam.IPRange',
        blank=True,
        related_name="%(class)s_source_ranges",
    )
    destination_ranges = models.ManyToManyField(
        to='ipam.IPRange',
        blank=True,
        related_name="%(class)s_destination_ranges",
    )
    source_pool = models.ForeignKey(
        to='netbox_security.NatPool',
        on_delete=models.PROTECT,
        null=True,
        related_name="%(class)s_source_pool",
    )
    destination_pool = models.ForeignKey(
        to='netbox_security.NatPool',
        on_delete=models.PROTECT,
        null=True,
        related_name="%(class)s_destination_pool",
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
    custom_interface = models.CharField(
        max_length=50,
        choices=CustomInterfaceChoices,
        default=CustomInterfaceChoices.NONE,
        blank=True,
        null=True,
    )

    prerequisite_models = (
        'dcim.Interface',
        'netbox_security.NatPool',
        'netbox_security.NatRuleSet',
    )

    class Meta:
        verbose_name_plural = _('NAT Rules')
        unique_together = ['rule_set', 'name']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_security:natrule', args=[self.pk])

    def get_status_color(self):
        return RuleStatusChoices.colors.get(self.status)

    @property
    def source_port_list(self):
        return array_to_string(self.source_ports)

    @property
    def destination_port_list(self):
        return array_to_string(self.destination_ports)


class NatRuleAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=RULE_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField(blank=True, null=True,)
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type",
        fk_field="assigned_object_id",
    )
    rule = models.ForeignKey(
        to='netbox_security.NatRule',
        on_delete=models.CASCADE
    )

    clone_fields = ('assigned_object_type', 'assigned_object_id')

    prerequisite_models = (
        'dcim.Device',
        'netbox_security.NatRule',
    )

    class Meta:
        indexes = (
            models.Index(fields=('assigned_object_type', 'assigned_object_id')),
        )
        constraints = (
            models.UniqueConstraint(
                fields=('assigned_object_type', 'assigned_object_id', 'rule'),
                name='%(app_label)s_%(class)s_unique_interface_rule'
            ),
        )
        verbose_name = _('NAT Pool assignment')
        verbose_name_plural = _('NAT Ruleset assignments')

    def __str__(self):
        return f'{self.assigned_object}: {self.rule}'

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class NatRuleIndex(SearchIndex):
    model = NatRule
    fields = (
        ("name", 100),
    )


GenericRelation(
    to=NatRuleAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="interface",
).contribute_to_class(Interface, "natrules")
