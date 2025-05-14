import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ChoiceFieldColumn

from netbox_security.models import NatPoolMember


__all__ = ("NatPoolMemberTable",)


class NatPoolMemberTable(NetBoxTable):
    name = tables.LinkColumn()
    pool = tables.LinkColumn()
    status = ChoiceFieldColumn()
    address = tables.LinkColumn()
    prefix = tables.LinkColumn()
    address_range = tables.LinkColumn()
    source_ports = tables.Column(
        accessor=tables.A("source_port_list"),
        order_by=tables.A("source_ports"),
    )
    destination_ports = tables.Column(
        accessor=tables.A("destination_port_list"),
        order_by=tables.A("destination_ports"),
    )
    tags = TagColumn(url_name="plugins:netbox_security:natpoolmember_list")

    class Meta(NetBoxTable.Meta):
        model = NatPoolMember
        fields = (
            "pk",
            "name",
            "pool",
            "status",
            "address",
            "prefix",
            "address_range",
            "source_ports",
            "destination_ports",
            "tags",
        )
        default_columns = (
            "name",
            "status",
            "pool",
            "address",
            "prefix",
            "address_range",
            "source_ports",
            "destination_ports",
        )
