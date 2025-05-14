import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ChoiceFieldColumn
from tenancy.tables import TenancyColumnsMixin

from netbox_security.models import Policer


__all__ = ("PolicerTable",)


class PolicerTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.LinkColumn()
    logical_interface_policer = tables.BooleanColumn()
    physical_interface_policer = tables.BooleanColumn()
    bandwidth_limit = tables.Column()
    bandwidth_percent = tables.Column()
    burst_size_limit = tables.Column()
    loss_priority = ChoiceFieldColumn()
    forwarding_class = ChoiceFieldColumn()
    discard = tables.BooleanColumn()
    out_of_profile = tables.BooleanColumn()

    tags = TagColumn(url_name="plugins:netbox_security:policer_list")

    class Meta(NetBoxTable.Meta):
        model = Policer
        fields = (
            "pk",
            "name",
            "description",
            "logical_interface_policer",
            "physical_interface_policer",
            "bandwidth_limit",
            "bandwidth_percent",
            "burst_size_limit",
            "loss_priority",
            "forwarding_class",
            "discard",
            "out_of_profile",
            "tenant",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "description",
            "logical_interface_policer",
            "physical_interface_policer",
            "bandwidth_limit",
            "bandwidth_percent",
            "burst_size_limit",
            "loss_priority",
            "forwarding_class",
            "discard",
            "out_of_profile",
            "tenant",
            "tags",
        )
