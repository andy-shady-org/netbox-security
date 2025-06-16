import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import ChoiceFieldColumn, TagColumn, ActionsColumn

from netbox_security.models import NatPool, NatPoolAssignment


__all__ = (
    "NatPoolTable",
    "NatPoolDeviceAssignmentTable",
    "NatPoolVirtualDeviceContextAssignmentTable",
    "NatPoolVirtualMachineAssignmentTable",
)


class NatPoolTable(NetBoxTable):
    name = tables.LinkColumn()
    pool_type = ChoiceFieldColumn()
    status = ChoiceFieldColumn()
    description = tables.LinkColumn()
    member_count = tables.Column()
    tags = TagColumn(url_name="plugins:netbox_security:natpool_list")

    class Meta(NetBoxTable.Meta):
        model = NatPool
        fields = ("pk", "name", "pool_type", "member_count", "description", "tags")
        default_columns = ("pk", "name", "pool_type", "member_count", "description")


class NatPoolDeviceAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Device"),
    )
    pool = tables.Column(verbose_name=_("NAT Pool"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = NatPoolAssignment
        fields = ("pk", "pool", "assigned_object")
        exclude = ("id",)


class NatPoolVirtualDeviceContextAssignmentTable(NetBoxTable):
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
    pool = tables.Column(verbose_name=_("NAT Pool"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = NatPoolAssignment
        fields = ("pk", "pool", "assigned_object", "assigned_object_parent")
        exclude = ("id",)


class NatPoolVirtualMachineAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Virtual Machine"),
    )
    pool = tables.Column(verbose_name=_("NAT Pool"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = NatPoolAssignment
        fields = ("pk", "pool", "assigned_object", "assigned_object_parent")
        exclude = ("id",)
