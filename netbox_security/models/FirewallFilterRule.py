from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from netbox.models.features import ContactsMixin
from netbox.models import PrimaryModel
from netbox.search import SearchIndex, register_search

from netbox_security.mixins import FirewallRuleSettingMixin


__all__ = (
    'FirewallRuleFromSetting',
    'FirewallRuleThenSetting',
    'FirewallFilterRule',
    'FirewallFilterRuleIndex',
)


class FirewallRuleFromSetting(FirewallRuleSettingMixin):
    class Meta:
        verbose_name = _('Firewall Filter Rule Setting')

    def get_absolute_url(self):
        return reverse('plugins:netbox_security:firewallrulefromsetting', args=[self.pk])


class FirewallRuleThenSetting(FirewallRuleSettingMixin):
    class Meta:
        verbose_name = _('Firewall Filter Rule Setting')

    def get_absolute_url(self):
        return reverse('plugins:netbox_security:firewallrulethensetting', args=[self.pk])


class FirewallFilterRule(ContactsMixin, PrimaryModel):
    name = models.CharField(
        max_length=200
    )
    filter = models.ForeignKey(
        to='netbox_security.FirewallFilter',
        on_delete=models.CASCADE,
        related_name="%(class)s_rules"
    )
    index = models.PositiveIntegerField()
    from_settings = GenericRelation(
        to='netbox_security.FirewallRuleFromSetting',
        related_name='from_settings',
        related_query_name='from_settings',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id'
    )
    then_settings = GenericRelation(
        to='netbox_security.FirewallRuleThenSetting',
        related_name='then_settings',
        related_query_name='then_settings',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id'
    )

    class Meta:
        verbose_name = 'Firewall Filter Rule'
        ordering = ['index', 'name']

    def __str__(self):
        return f'{self.filter}: {self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_security:firewallfilterrule', args=[self.pk])


@register_search
class FirewallFilterRuleIndex(SearchIndex):
    model = FirewallFilterRule
    fields = (
        ("name", 100),
        ("filter", 300),
        ("description", 500),
    )
