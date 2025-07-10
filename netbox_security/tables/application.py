import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import (
    TagColumn,
    ActionsColumn,
    ManyToManyColumn,
)
from tenancy.tables import TenancyColumnsMixin

from netbox_security.models import Application, ApplicationAssignment


__all__ = (
    "ApplicationTable",
    "ApplicationAssignmentTable",
)


class ApplicationTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.LinkColumn()
    application_items = ManyToManyColumn(
        linkify_item=True,
        orderable=False,
        linkify=True,
        verbose_name=_("Application Items"),
    )
    protocol = tables.Column(
        accessor=tables.A("protocol_list"),
        order_by=tables.A("protocol"),
    )
    source_ports = tables.Column(
        accessor=tables.A("source_port_list"),
        order_by=tables.A("source_ports"),
    )
    destination_ports = tables.Column(
        accessor=tables.A("destination_port_list"),
        order_by=tables.A("destination_ports"),
    )
    tags = TagColumn(url_name="plugins:netbox_security:application_list")

    class Meta(NetBoxTable.Meta):
        model = Application
        fields = (
            "id",
            "name",
            "identifier",
            "description",
            "application_items",
            "protocol",
            "destination_ports",
            "source_ports",
            "tenant",
            "tags",
        )
        default_columns = (
            "name",
            "identifier",
            "description",
            "application_items",
            "protocol",
            "destination_ports",
            "source_ports",
            "tenant",
        )


class ApplicationAssignmentTable(NetBoxTable):
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
    application = tables.Column(verbose_name=_("Application"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = ApplicationAssignment
        fields = ("id", "application", "assigned_object", "assigned_object_parent")
        default_columns = ("application", "assigned_object", "assigned_object_parent")
