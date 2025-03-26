import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ArrayColumn, ChoicesColumn
from tenancy.tables import TenancyColumnsMixin

from netbox_security.models import SecurityZonePolicy


__all__ = (
    "SecurityZonePolicyTable",
)


class SecurityZonePolicyTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.LinkColumn()
    source_zone = tables.LinkColumn()
    destination_zone = tables.LinkColumn()
    source_address = ArrayColumn()
    destination_address = ArrayColumn()
    actions = ChoicesColumn()
    tags = TagColumn(
        url_name='plugins:netbox_security:securityzone_list'
    )

    class Meta(NetBoxTable.Meta):
        model = SecurityZonePolicy
        fields = ('pk', 'name', 'source_zone', 'destination_zone', 'source_address',
                  'destination_address', 'application', 'actions', 'description', 'tenant', 'tags')
        default_columns = (
            'pk', 'name', 'source_zone', 'destination_zone', 'source_address',
            'destination_address', 'application', 'actions', 'tenant', 'tags',
        )
