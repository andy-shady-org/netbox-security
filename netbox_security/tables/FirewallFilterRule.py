import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn

from netbox_security.models import FirewallFilterRule, FirewallRuleFromSetting


__all__ = (
    "FirewallFilterRuleTable",
    "FirewallRuleFromSettingTable",
    "FirewallRuleThenSettingTable",
)


class FirewallFilterRuleTable(NetBoxTable):
    name = tables.LinkColumn()
    filter = tables.LinkColumn()
    tags = TagColumn(url_name="plugins:netbox_security:addresslist_list")

    class Meta(NetBoxTable.Meta):
        model = FirewallFilterRule
        fields = ("pk", "id", "name", "index", "filter")
        default_columns = ("pk", "id", "name", "index", "filter")


class FirewallRuleFromSettingTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = FirewallRuleFromSetting
        fields = ("pk", "id", "assigned_object", "key", "value")
        default_columns = ("pk", "id", "assigned_object", "key", "value")


class FirewallRuleThenSettingTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = FirewallRuleFromSetting
        fields = ("pk", "id", "assigned_object", "key", "value")
        default_columns = ("pk", "id", "assigned_object", "key", "value")
