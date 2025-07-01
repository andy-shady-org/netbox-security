import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ActionsColumn, ManyToManyColumn
from tenancy.tables import TenancyColumnsMixin

from netbox_security.models import AddressSet, AddressSetAssignment


__all__ = (
    "AddressSetTable",
    "AddressSetDeviceAssignmentTable",
    "AddressSetVirtualDeviceContextAssignmentTable",
    "AddressSetSecurityZoneAssignmentTable",
)


class AddressSetTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.LinkColumn()
    addresses = ManyToManyColumn(
        orderable=False, linkify=True, verbose_name=_("Addresses")
    )
    tags = TagColumn(url_name="plugins:netbox_security:addressset_list")

    class Meta(NetBoxTable.Meta):
        model = AddressSet
        fields = (
            "pk",
            "name",
            "identifier",
            "description",
            "addresses",
            "tenant",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "identifier",
            "description",
            "addresses",
            "tenant",
        )


class AddressSetDeviceAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Device"),
    )
    address_set = tables.Column(verbose_name=_("AddressSet"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = AddressSetAssignment
        fields = ("pk", "address_set", "assigned_object")
        exclude = ("id",)


class AddressSetVirtualDeviceContextAssignmentTable(NetBoxTable):
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
    address_set = tables.Column(verbose_name=_("AddressSet"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = AddressSetAssignment
        fields = ("pk", "address_set", "assigned_object", "assigned_object_parent")
        exclude = ("id",)


class AddressSetSecurityZoneAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Security Zone"),
    )
    address_set = tables.Column(verbose_name=_("AddressSet"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = AddressSetAssignment
        fields = ("pk", "address_set", "assigned_object")
        exclude = ("id",)
