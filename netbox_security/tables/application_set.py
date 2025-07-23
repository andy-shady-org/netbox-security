import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ActionsColumn, ManyToManyColumn
from tenancy.tables import TenancyColumnsMixin

from netbox_security.models import ApplicationSet, ApplicationSetAssignment


__all__ = (
    "ApplicationSetTable",
    "ApplicationSetAssignmentTable",
)


class ApplicationSetTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.LinkColumn()
    applications = ManyToManyColumn(
        linkify_item=True,
        orderable=False,
        linkify=True,
        verbose_name=_("Applications"),
    )
    application_sets = ManyToManyColumn(
        linkify_item=True,
        orderable=False,
        linkify=True,
        verbose_name=_("Application Sets"),
    )
    tags = TagColumn(url_name="plugins:netbox_security:applicationset_list")

    class Meta(NetBoxTable.Meta):
        model = ApplicationSet
        fields = (
            "id",
            "name",
            "identifier",
            "description",
            "applications",
            "application_sets",
            "tenant",
            "tags",
        )
        default_columns = (
            "name",
            "identifier",
            "description",
            "applications",
            "application_sets",
            "tenant",
        )


class ApplicationSetAssignmentTable(NetBoxTable):
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
    application_set = tables.Column(verbose_name=_("Application Set"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = ApplicationSetAssignment
        fields = ("id", "application_set", "assigned_object", "assigned_object_parent")
        default_columns = (
            "application_set",
            "assigned_object",
            "assigned_object_parent",
        )
