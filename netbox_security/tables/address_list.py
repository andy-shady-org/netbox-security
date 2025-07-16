import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import ActionsColumn

from netbox_security.models import AddressList, AddressListAssignment


__all__ = (
    "AddressListTable",
    "AddressListAssignmentTable",
)


class AddressListTable(NetBoxTable):
    name = tables.LinkColumn()
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Assigned Object"),
    )
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = AddressList
        fields = ("pk", "name", "assigned_object")
        exclude = ("id",)


class AddressListAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Assigned Object"),
    )
    address_list = tables.Column(verbose_name=_("Address List"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = AddressListAssignment
        fields = (
            "id",
            "address_list",
            "assigned_object",
        )
        default_columns = (
            "address_list",
            "assigned_object",
        )
