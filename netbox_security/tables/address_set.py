import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ActionsColumn, ManyToManyColumn
from tenancy.tables import TenancyColumnsMixin

from netbox_security.models import AddressSet, AddressSetAssignment


__all__ = (
    "AddressSetTable",
    "AddressSetAssignmentTable",
)


class AddressSetTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.LinkColumn()
    addresses = ManyToManyColumn(
        linkify_item=True,
        orderable=False,
        linkify=True,
        verbose_name=_("Addresses"),
    )
    address_sets = ManyToManyColumn(
        linkify_item=True,
        orderable=False,
        linkify=True,
        verbose_name=_("Address Sets"),
    )
    tags = TagColumn(url_name="plugins:netbox_security:addressset_list")

    class Meta(NetBoxTable.Meta):
        model = AddressSet
        fields = (
            "id",
            "name",
            "identifier",
            "description",
            "addresses",
            "address_sets",
            "tenant",
            "tags",
        )
        default_columns = (
            "name",
            "identifier",
            "description",
            "addresses",
            "address_sets",
            "tenant",
        )


class AddressSetAssignmentTable(NetBoxTable):
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
    address_set = tables.Column(verbose_name=_("AddressSet"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = AddressSetAssignment
        fields = ("id", "address_set", "assigned_object", "assigned_object_parent")
        default_columns = ("address_set", "assigned_object", "assigned_object_parent")
