import django_tables2 as tables

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
    firewall_filter = tables.LinkColumn()
    tags = TagColumn(url_name="plugins:netbox_security:firewallfilterrule_list")

    class Meta(NetBoxTable.Meta):
        model = FirewallFilterRule
        fields = ("pk", "name", "index", "firewall_filter", "tags")
        default_columns = ("pk", "name", "index", "firewall_filter")


class FirewallRuleFromSettingTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = FirewallRuleFromSetting
        fields = ("pk", "assigned_object", "key", "value")
        default_columns = ("pk", "assigned_object", "key", "value")


class FirewallRuleThenSettingTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = FirewallRuleFromSetting
        fields = ("pk", "assigned_object", "key", "value")
        default_columns = ("pk", "assigned_object", "key", "value")
