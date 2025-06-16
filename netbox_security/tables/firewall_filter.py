import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ActionsColumn, ChoiceFieldColumn
from tenancy.tables import TenancyColumnsMixin

from netbox_security.models import FirewallFilter, FirewallFilterAssignment


__all__ = (
    "FirewallFilterTable",
    "FirewallFilterDeviceAssignmentTable",
    "FirewallFilterVirtualDeviceContextAssignmentTable",
)


class FirewallFilterTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.LinkColumn()
    family = ChoiceFieldColumn(verbose_name=_("Family"))
    rule_count = tables.Column()
    tags = TagColumn(url_name="plugins:netbox_security:firewallfilter_list")

    class Meta(NetBoxTable.Meta):
        model = FirewallFilter
        fields = ("pk", "name", "description", "family", "rule_count", "tenant", "tags")
        default_columns = (
            "pk",
            "name",
            "description",
            "family",
            "rule_count",
            "tenant",
        )


class FirewallFilterDeviceAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Device"),
    )
    firewall_filter = tables.Column(verbose_name=_("Firewall Filter"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = FirewallFilterAssignment
        fields = ("pk", "firewall_filter", "assigned_object")
        exclude = ("id",)


class FirewallFilterVirtualDeviceContextAssignmentTable(NetBoxTable):
    assigned_object_parent = tables.Column(
        accessor=tables.A("assigned_object__device"),
        linkify=True,
        orderable=False,
        verbose_name=_("Parent"),
    )
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Virtual Device Context"),
    )
    firewall_filter = tables.Column(verbose_name=_("Firewall Filter"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = FirewallFilterAssignment
        fields = ("pk", "firewall_filter", "assigned_object", "assigned_object_parent")
        exclude = ("id",)
