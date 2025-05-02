import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import (
    ChoiceFieldColumn,
    TagColumn,
    ActionsColumn,
    ManyToManyColumn,
)

from netbox_security.models import NatRule, NatRuleAssignment


__all__ = (
    "NatRuleTable",
    "NatRuleAssignmentTable",
)


class NatRuleTable(NetBoxTable):
    rule_set = tables.LinkColumn()
    name = tables.LinkColumn()
    pool = tables.LinkColumn()
    description = tables.LinkColumn()
    status = ChoiceFieldColumn()
    source_type = ChoiceFieldColumn()
    destination_type = ChoiceFieldColumn()
    custom_interface = ChoiceFieldColumn()
    source_addresses = ManyToManyColumn(
        orderable=False, linkify=True, verbose_name=_("Source Addresses")
    )
    destination_addresses = ManyToManyColumn(
        orderable=False, linkify=True, verbose_name=_("Destination Addresses")
    )
    source_prefixes = ManyToManyColumn(
        orderable=False, linkify=True, verbose_name=_("Source Prefixes")
    )
    destination_prefixes = ManyToManyColumn(
        orderable=False, linkify=True, verbose_name=_("Destination Prefixes")
    )
    source_ranges = ManyToManyColumn(
        orderable=False, linkify=True, verbose_name=_("Source Ranges")
    )
    destination_ranges = ManyToManyColumn(
        orderable=False, linkify=True, verbose_name=_("Destination Ranges")
    )
    source_ports = tables.Column(
        accessor=tables.A("source_port_list"),
        order_by=tables.A("source_ports"),
    )
    destination_ports = tables.Column(
        accessor=tables.A("destination_port_list"),
        order_by=tables.A("destination_ports"),
    )
    source_pool = tables.LinkColumn()
    destination_pool = tables.LinkColumn()
    tags = TagColumn(url_name="plugins:netbox_security:natrule_list")

    class Meta(NetBoxTable.Meta):
        model = NatRule
        fields = (
            "pk",
            "rule_set",
            "name",
            "description",
            "status",
            "custom_interface",
            "source_type",
            "destination_type",
            "source_addresses",
            "destination_addresses",
            "source_prefixes",
            "destination_prefixes",
            "source_ranges",
            "destination_ranges",
            "source_ports",
            "destination_ports",
            "pool",
            "source_pool",
            "destination_pool",
            "tags",
        )
        default_columns = ("pk", "name", "status", "rule_set", "description", "pool")


class NatRuleAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Interface"),
    )
    rule = tables.Column(verbose_name=_("NAT Rule"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = NatRuleAssignment
        fields = ("pk", "rule", "assigned_object")
        exclude = ("id",)
