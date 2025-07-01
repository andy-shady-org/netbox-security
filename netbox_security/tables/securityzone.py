import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ActionsColumn
from tenancy.tables import TenancyColumnsMixin

from netbox_security.models import SecurityZone, SecurityZoneAssignment


__all__ = (
    "SecurityZoneTable",
    "SecurityZoneDeviceAssignmentTable",
    "SecurityZoneVirtualDeviceContextAssignmentTable",
    "SecurityZoneInterfaceAssignmentTable",
)


class SecurityZoneTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.LinkColumn()
    source_policy_count = tables.Column()
    destination_policy_count = tables.Column()
    tags = TagColumn(url_name="plugins:netbox_security:securityzone_list")

    class Meta(NetBoxTable.Meta):
        model = SecurityZone
        fields = (
            "pk",
            "name",
            "identifier",
            "description",
            "source_policy_count",
            "destination_policy_count",
            "tenant",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "identifier",
            "description",
            "source_policy_count",
            "destination_policy_count",
            "tenant",
            "tags",
        )


class SecurityZoneDeviceAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Device"),
    )
    zone = tables.Column(verbose_name=_("Security Zone"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = SecurityZoneAssignment
        fields = ("pk", "zone", "assigned_object")
        exclude = ("id",)


class SecurityZoneVirtualDeviceContextAssignmentTable(NetBoxTable):
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
    zone = tables.Column(verbose_name=_("Security Zone"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = SecurityZoneAssignment
        fields = ("pk", "zone", "assigned_object", "assigned_object_parent")
        exclude = ("id",)


class SecurityZoneInterfaceAssignmentTable(NetBoxTable):
    assigned_object_parent = tables.Column(
        accessor=tables.A("assigned_object__device"),
        linkify=True,
        orderable=False,
        verbose_name=_("Parent"),
    )
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Interface"),
    )
    zone = tables.Column(verbose_name=_("Security Zone"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = SecurityZoneAssignment
        fields = ("pk", "zone", "assigned_object", "assigned_object_parent")
        exclude = ("id",)
