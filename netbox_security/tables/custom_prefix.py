import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn
from tenancy.tables import TenancyColumnsMixin

from netbox_security.models import CustomPrefix

__all__ = ("CustomPrefixTable",)


class CustomPrefixTable(TenancyColumnsMixin, NetBoxTable):
    prefix = tables.LinkColumn()
    tags = TagColumn(url_name="plugins:netbox_security:customprefix_list")

    class Meta(NetBoxTable.Meta):
        model = CustomPrefix
        fields = (
            "id",
            "prefix",
            "description",
            "tenant",
            "tags",
        )
        default_columns = (
            "prefix",
            "description",
            "tenant",
        )
