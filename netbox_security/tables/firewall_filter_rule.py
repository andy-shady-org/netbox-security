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
    filter = tables.LinkColumn()
    tags = TagColumn(url_name="plugins:netbox_security:firewallfilterrule_list")

    class Meta(NetBoxTable.Meta):
        model = FirewallFilterRule
        fields = ("pk", "id", "name", "index", "firewall_filter")
        default_columns = ("pk", "id", "name", "index", "firewall_filter")


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
