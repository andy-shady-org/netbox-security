import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ChoiceFieldColumn, ActionsColumn
from tenancy.tables import TenancyColumnsMixin

from netbox_security.models import Policer, PolicerAssignment


__all__ = (
    "PolicerTable",
    "PolicerDeviceAssignmentTable",
    "PolicerVirtualDeviceContextAssignmentTable",
)


class PolicerTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.LinkColumn()
    logical_interface_policer = tables.BooleanColumn()
    physical_interface_policer = tables.BooleanColumn()
    bandwidth_limit = tables.Column()
    bandwidth_percent = tables.Column()
    burst_size_limit = tables.Column()
    loss_priority = ChoiceFieldColumn()
    forwarding_class = ChoiceFieldColumn()
    discard = tables.BooleanColumn()
    out_of_profile = tables.BooleanColumn()

    tags = TagColumn(url_name="plugins:netbox_security:policer_list")

    class Meta(NetBoxTable.Meta):
        model = Policer
        fields = (
            "pk",
            "name",
            "description",
            "logical_interface_policer",
            "physical_interface_policer",
            "bandwidth_limit",
            "bandwidth_percent",
            "burst_size_limit",
            "loss_priority",
            "forwarding_class",
            "discard",
            "out_of_profile",
            "tenant",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "description",
            "logical_interface_policer",
            "physical_interface_policer",
            "bandwidth_limit",
            "bandwidth_percent",
            "burst_size_limit",
            "loss_priority",
            "forwarding_class",
            "discard",
            "out_of_profile",
            "tenant",
            "tags",
        )


class PolicerDeviceAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Device"),
    )
    policer = tables.Column(verbose_name=_("Policer"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = PolicerAssignment
        fields = ("pk", "policer", "assigned_object")
        exclude = ("id",)


class PolicerVirtualDeviceContextAssignmentTable(NetBoxTable):
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
    policer = tables.Column(verbose_name=_("Policer"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = PolicerAssignment
        fields = ("pk", "policer", "assigned_object", "assigned_object_parent")
        exclude = ("id",)
