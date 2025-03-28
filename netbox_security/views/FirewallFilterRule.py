from netbox.views import generic
from tenancy.views import ObjectContactsView
from utilities.views import register_model_view

from netbox_security.tables import (
    FirewallFilterRuleTable,
    FirewallRuleFromSettingTable,
    FirewallRuleThenSettingTable,
)

from netbox_security.filtersets import FirewallFilterRuleFilterSet

from netbox_security.models import (
    FirewallFilterRule,
    FirewallRuleFromSetting,
    FirewallRuleThenSetting,
)
from netbox_security.forms import (
    FirewallFilterRuleFilterForm,
    FirewallFilterRuleForm,
)


__all__ = (
    'FirewallFilterRuleView',
    'FirewallFilterRuleListView',
    'FirewallFilterRuleEditView',
    'FirewallFilterRuleDeleteView',
    'FirewallFilterRuleBulkDeleteView',
    'FirewallFilterRuleContactsView',
    'FirewallRuleFromSettingDeleteView',
    'FirewallRuleFromSettingBulkDeleteView',
    'FirewallRuleThenSettingDeleteView',
    'FirewallRuleThenSettingBulkDeleteView',
)


class FirewallFilterRuleView(generic.ObjectView):
    queryset = FirewallFilterRule.objects.all()
    template_name = 'netbox_security/firewallfilterrule.html'


class FirewallFilterRuleListView(generic.ObjectListView):
    queryset = FirewallFilterRule.objects.all()
    filterset = FirewallFilterRuleFilterSet
    filterset_form = FirewallFilterRuleFilterForm
    table = FirewallFilterRuleTable


class FirewallFilterRuleEditView(generic.ObjectEditView):
    queryset = FirewallFilterRule.objects.all()
    form = FirewallFilterRuleForm


class FirewallFilterRuleDeleteView(generic.ObjectDeleteView):
    queryset = FirewallFilterRule.objects.all()
    default_return_url = 'plugins:netbox_security:firewallfilterrule_list'


class FirewallFilterRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = FirewallFilterRule.objects.all()
    table = FirewallFilterRuleTable
    default_return_url = 'plugins:netbox_security:firewallfilterrule_list'


@register_model_view(FirewallFilterRule, "contacts")
class FirewallFilterRuleContactsView(ObjectContactsView):
    queryset = FirewallFilterRule.objects.all()


class FirewallRuleFromSettingDeleteView(generic.ObjectDeleteView):
    queryset = FirewallRuleFromSetting.objects.all()
    default_return_url = 'plugins:netbox_security:firewallfilterrule_list'


class FirewallRuleFromSettingBulkDeleteView(generic.BulkDeleteView):
    queryset = FirewallFilterRule.objects.all()
    table = FirewallRuleFromSettingTable
    default_return_url = 'plugins:netbox_security:firewallfilterrule_list'


class FirewallRuleThenSettingDeleteView(generic.ObjectDeleteView):
    queryset = FirewallRuleThenSetting.objects.all()
    default_return_url = 'plugins:netbox_security:firewallfilterrule_list'


class FirewallRuleThenSettingBulkDeleteView(generic.BulkDeleteView):
    queryset = FirewallRuleThenSetting.objects.all()
    table = FirewallRuleThenSettingTable
    default_return_url = 'plugins:netbox_security:firewallfilterrule_list'