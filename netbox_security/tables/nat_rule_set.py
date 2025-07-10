import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import (
    ChoiceFieldColumn,
    TagColumn,
    ActionsColumn,
    ManyToManyColumn,
)

from netbox_security.models import NatRuleSet, NatRuleSetAssignment


__all__ = (
    "NatRuleSetTable",
    "NatRuleSetAssignmentTable",
)


class NatRuleSetTable(NetBoxTable):
    name = tables.LinkColumn()
    description = tables.LinkColumn()
    nat_type = ChoiceFieldColumn()
    source_zones = ManyToManyColumn(
        linkify_item=True,
        orderable=False,
        linkify=True,
        verbose_name=_("Source Zones"),
    )
    destination_zones = ManyToManyColumn(
        linkify_item=True,
        orderable=False,
        linkify=True,
        verbose_name=_("Destination Zones"),
    )
    direction = ChoiceFieldColumn()
    rule_count = tables.Column()
    tags = TagColumn(url_name="plugins:netbox_security:natruleset_list")

    class Meta(NetBoxTable.Meta):
        model = NatRuleSet
        fields = (
            "id",
            "name",
            "description",
            "nat_type",
            "rule_count",
            "source_zones",
            "destination_zones",
            "direction",
            "tags",
        )
        default_columns = (
            "name",
            "description",
            "nat_type",
            "rule_count",
            "direction",
            "source_zones",
            "destination_zones",
        )


class NatRuleSetAssignmentTable(NetBoxTable):
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
    ruleset = tables.Column(verbose_name=_("NAT Ruleset"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = NatRuleSetAssignment
        fields = ("id", "ruleset", "assigned_object", "assigned_object_parent")
        default_columns = ("ruleset", "assigned_object", "assigned_object_parent")
