from netbox.views import generic
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
    FirewallFilterRuleBulkEditForm,
    FirewallFilterRuleImportForm,
)


__all__ = (
    "FirewallFilterRuleView",
    "FirewallFilterRuleListView",
    "FirewallFilterRuleEditView",
    "FirewallFilterRuleDeleteView",
    "FirewallFilterRuleBulkEditView",
    "FirewallFilterRuleBulkDeleteView",
    "FirewallRuleFromSettingView",
    "FirewallRuleFromSettingDeleteView",
    "FirewallRuleFromSettingBulkDeleteView",
    "FirewallFilterRuleBulkImportView",
    "FirewallRuleThenSettingView",
    "FirewallRuleThenSettingDeleteView",
    "FirewallRuleThenSettingBulkDeleteView",
)


@register_model_view(FirewallFilterRule)
class FirewallFilterRuleView(generic.ObjectView):
    queryset = FirewallFilterRule.objects.all()
    template_name = "netbox_security/firewallfilterrule.html"


@register_model_view(FirewallFilterRule, "list", path="", detail=False)
class FirewallFilterRuleListView(generic.ObjectListView):
    queryset = FirewallFilterRule.objects.all()
    filterset = FirewallFilterRuleFilterSet
    filterset_form = FirewallFilterRuleFilterForm
    table = FirewallFilterRuleTable


@register_model_view(FirewallFilterRule, "add", detail=False)
@register_model_view(FirewallFilterRule, "edit")
class FirewallFilterRuleEditView(generic.ObjectEditView):
    queryset = FirewallFilterRule.objects.all()
    form = FirewallFilterRuleForm


@register_model_view(FirewallFilterRule, "delete")
class FirewallFilterRuleDeleteView(generic.ObjectDeleteView):
    queryset = FirewallFilterRule.objects.all()


@register_model_view(FirewallFilterRule, "bulk_edit", path="edit", detail=False)
class FirewallFilterRuleBulkEditView(generic.BulkEditView):
    queryset = FirewallFilterRule.objects.all()
    filterset = FirewallFilterRuleFilterSet
    table = FirewallFilterRuleTable
    form = FirewallFilterRuleBulkEditForm


@register_model_view(FirewallFilterRule, "bulk_delete", path="delete", detail=False)
class FirewallFilterRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = FirewallFilterRule.objects.all()
    table = FirewallFilterRuleTable


@register_model_view(FirewallRuleFromSetting)
class FirewallRuleFromSettingView(generic.ObjectView):
    queryset = FirewallRuleFromSetting.objects.all()


@register_model_view(FirewallRuleFromSetting, "delete")
class FirewallRuleFromSettingDeleteView(generic.ObjectDeleteView):
    queryset = FirewallRuleFromSetting.objects.all()


@register_model_view(FirewallRuleFromSetting, "bulk_delete", path="delete")
class FirewallRuleFromSettingBulkDeleteView(generic.BulkDeleteView):
    queryset = FirewallFilterRule.objects.all()
    table = FirewallRuleFromSettingTable


@register_model_view(FirewallFilterRule, "bulk_import", detail=False)
class FirewallFilterRuleBulkImportView(generic.BulkImportView):
    queryset = FirewallFilterRule.objects.all()
    model_form = FirewallFilterRuleImportForm


@register_model_view(FirewallRuleThenSetting)
class FirewallRuleThenSettingView(generic.ObjectView):
    queryset = FirewallRuleThenSetting.objects.all()


@register_model_view(FirewallRuleThenSetting, "delete")
class FirewallRuleThenSettingDeleteView(generic.ObjectDeleteView):
    queryset = FirewallRuleThenSetting.objects.all()


@register_model_view(FirewallRuleThenSetting, "bulk_delete", path="delete")
class FirewallRuleThenSettingBulkDeleteView(generic.BulkDeleteView):
    queryset = FirewallRuleThenSetting.objects.all()
    table = FirewallRuleThenSettingTable
