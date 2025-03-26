from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin
from dcim.models import Device, VirtualDeviceContext
from ipam.fields import IPNetworkField
from netbox.search import SearchIndex, register_search

from netbox_security.constants import FILTER_SETTING_ASSIGNMENT_MODELS
from netbox_security.choices import FirewallRuleSettingChoices


class FirewallRuleSetting(PrimaryModel):
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=FILTER_SETTING_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    assigned_object_id = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type',
        fk_field='assigned_object_id'
    )
    key = models.CharField(
        choices=FirewallRuleSettingChoices,
    )
    value = models.CharField()

    class Meta:
        verbose_name = 'Firewall Filter Rule Setting'

    def __str__(self):
        return f'{self.assigned_object}: {self.key}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('plugins:netbox_security:firewallrulesetting', args=[self.pk])


class FirewallFilterRule(PrimaryModel):
    name = models.CharField(
        max_length=200
    )
    filter = models.ForeignKey(
        to='netbox_security.FirewallFilter',
        on_delete=models.CASCADE,
        related_name="%(class)s_rules"
    )
    from_settings = GenericRelation(
        to='netbox_security.FirewallRuleSetting',
        related_name='from_settings',
        related_query_name='from_settings',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id'
    )
    then_settings = GenericRelation(
        to='netbox_security.FirewallRuleSetting',
        related_name='then_settings',
        related_query_name='then_settings',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id'
    )

    class Meta:
        verbose_name = 'Firewall Filter Rule'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('plugins:netbox_security:firewallfilterrule', args=[self.pk])
