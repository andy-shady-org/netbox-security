import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ActionsColumn
from tenancy.tables import TenancyColumnsMixin

from netbox_security.models import Address, AddressAssignment


__all__ = (
    "AddressTable",
    "AddressAssignmentTable",
)


class AddressTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.LinkColumn()
    tags = TagColumn(url_name="plugins:netbox_security:address_list")

    class Meta(NetBoxTable.Meta):
        model = Address
        fields = (
            "id",
            "name",
            "identifier",
            "description",
            "address",
            "dns_name",
            "ip_range",
            "tenant",
            "tags",
        )
        default_columns = (
            "name",
            "identifier",
            "description",
            "address",
            "dns_name",
            "ip_range",
            "tenant",
        )


class AddressAssignmentTable(NetBoxTable):
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
    address = tables.Column(verbose_name=_("Address"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = AddressAssignment
        fields = ("id", "address", "assigned_object", "assigned_object_parent")
        default_columns = ("address", "assigned_object", "assigned_object_parent")
