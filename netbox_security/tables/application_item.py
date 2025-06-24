import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn

from netbox_security.models import ApplicationItem


__all__ = ("ApplicationItemTable",)


class ApplicationItemTable(NetBoxTable):
    name = tables.LinkColumn()
    tags = TagColumn(url_name="plugins:netbox_security:applicationitem_list")

    class Meta(NetBoxTable.Meta):
        model = ApplicationItem
        fields = (
            "pk",
            "name",
            "index",
            "description",
            "protocol",
            "destination_port",
            "source_port",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "index",
            "description",
            "protocol",
            "destination_port",
            "source_port",
        )
