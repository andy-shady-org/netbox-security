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
    "NatRuleSetDeviceAssignmentTable",
    "NatRuleSetVirtualDeviceContextAssignmentTable",
    "NatRuleSetVirtualMachineAssignmentTable",
)


class NatRuleSetTable(NetBoxTable):
    name = tables.LinkColumn()
    description = tables.LinkColumn()
    nat_type = ChoiceFieldColumn()
    source_zones = ManyToManyColumn(
        orderable=False, linkify=True, verbose_name=_("Source Zones")
    )
    destination_zones = ManyToManyColumn(
        orderable=False, linkify=True, verbose_name=_("Destination Zones")
    )
    direction = ChoiceFieldColumn()
    rule_count = tables.Column()
    tags = TagColumn(url_name="plugins:netbox_security:natruleset_list")

    class Meta(NetBoxTable.Meta):
        model = NatRuleSet
        fields = (
            "pk",
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
            "pk",
            "name",
            "description",
            "nat_type",
            "rule_count",
            "direction",
        )


class NatRuleSetDeviceAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Device"),
    )
    ruleset = tables.Column(verbose_name=_("NAT Ruleset"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = NatRuleSetAssignment
        fields = ("pk", "ruleset", "assigned_object")
        exclude = ("id",)


class NatRuleSetVirtualDeviceContextAssignmentTable(NetBoxTable):
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
    ruleset = tables.Column(verbose_name=_("NAT Ruleset"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = NatRuleSetAssignment
        fields = ("pk", "ruleset", "assigned_object", "assigned_object_parent")
        exclude = ("id",)


class NatRuleSetVirtualMachineAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Virtual Machine"),
    )
    ruleset = tables.Column(verbose_name=_("NAT Ruleset"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = NatRuleSetAssignment
        fields = ("pk", "ruleset", "assigned_object", "assigned_object_parent")
        exclude = ("id",)
