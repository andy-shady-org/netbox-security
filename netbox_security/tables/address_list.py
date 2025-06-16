import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import ActionsColumn

from netbox_security.models import AddressList, AddressListAssignment


__all__ = (
    "AddressListTable",
    "AddressListAddressTable",
    "AddressListAddressSetTable",
    "AddressListDeviceAssignmentTable",
    "AddressListVirtualDeviceContextAssignmentTable",
    "AddressListSecurityZoneAssignmentTable",
)


class AddressListTable(NetBoxTable):
    name = tables.LinkColumn()
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Addresses/Address Sets"),
    )
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = AddressList
        fields = ("pk", "name", "assigned_object")
        exclude = ("id",)


class AddressListAddressTable(NetBoxTable):
    name = tables.LinkColumn()
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Addresses"),
    )
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = AddressList
        fields = ("pk", "name", "assigned_object")
        exclude = ("id",)


class AddressListAddressSetTable(NetBoxTable):
    name = tables.LinkColumn()
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Address Sets"),
    )
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = AddressList
        fields = ("pk", "name", "assigned_object")
        exclude = ("id",)


class AddressListDeviceAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Device"),
    )
    address_list = tables.Column(verbose_name=_("Address List"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = AddressListAssignment
        fields = ("pk", "address", "assigned_object")
        exclude = ("id",)


class AddressListVirtualDeviceContextAssignmentTable(NetBoxTable):
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
    address_list = tables.Column(verbose_name=_("Address List"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = AddressListAssignment
        fields = ("pk", "address", "assigned_object", "assigned_object_parent")
        exclude = ("id",)


class AddressListSecurityZoneAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Security Zone"),
    )
    address_list = tables.Column(verbose_name=_("Address List"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = AddressListAssignment
        fields = ("pk", "address_list", "assigned_object")
        exclude = ("id",)
