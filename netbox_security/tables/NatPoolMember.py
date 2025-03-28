import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ChoiceFieldColumn

from netbox_security.models import NatPoolMember

CHOICE_LABEL = mark_safe('<span class="label label-info">{{ value }}</span>')

__all__ = ("NatPoolMemberTable",)


class NatPoolMemberTable(NetBoxTable):
    name = tables.LinkColumn()
    pool = tables.LinkColumn()
    status = ChoiceFieldColumn(default=CHOICE_LABEL, verbose_name=_("Status"))
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
            "address",
            "prefix",
            "address_range",
            "source_ports",
            "destination_ports",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "address",
            "prefix",
            "address_range",
            "source_ports",
            "destination_ports",
        )
