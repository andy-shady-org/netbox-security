import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ActionsColumn, ChoiceFieldColumn
from tenancy.tables import TenancyColumnsMixin

from netbox_security.models import FirewallFilter, FirewallFilterAssignment


__all__ = (
    "FirewallFilterTable",
    "FirewallFilterAssignmentTable",
)


class FirewallFilterTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.LinkColumn()
    family = ChoiceFieldColumn(verbose_name=_("Family"))
    rule_count = tables.Column()
    tags = TagColumn(url_name="plugins:netbox_security:firewallfilter_list")

    class Meta(NetBoxTable.Meta):
        model = FirewallFilter
        fields = (
            "id",
            "name",
            "description",
            "family",
            "rule_count",
            "tenant",
            "tags",
        )
        default_columns = (
            "name",
            "description",
            "family",
            "rule_count",
            "tenant",
        )


class FirewallFilterAssignmentTable(NetBoxTable):
    assigned_object_parent = tables.Column(
        accessor=tables.A("assigned_object__device"),
        linkify=True,
        orderable=False,
        verbose_name=_("Parent"),
    )
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Assigned Object"),
    )
    firewall_filter = tables.Column(verbose_name=_("Firewall Filter"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = FirewallFilterAssignment
        fields = ("id", "firewall_filter", "assigned_object", "assigned_object_parent")
        default_columns = (
            "firewall_filter",
            "assigned_object",
            "assigned_object_parent",
        )
