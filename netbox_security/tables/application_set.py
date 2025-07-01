import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ActionsColumn, ManyToManyColumn
from tenancy.tables import TenancyColumnsMixin

from netbox_security.models import ApplicationSet, ApplicationSetAssignment


__all__ = (
    "ApplicationSetTable",
    "ApplicationSetDeviceAssignmentTable",
    "ApplicationSetVirtualDeviceContextAssignmentTable",
)


class ApplicationSetTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.LinkColumn()
    applications = ManyToManyColumn(
        orderable=False, linkify=True, verbose_name=_("Applications")
    )
    tags = TagColumn(url_name="plugins:netbox_security:applicationset_list")

    class Meta(NetBoxTable.Meta):
        model = ApplicationSet
        fields = (
            "pk",
            "name",
            "identifier",
            "description",
            "applications",
            "tenant",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "identifier",
            "description",
            "applications",
            "tenant",
        )


class ApplicationSetDeviceAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Device"),
    )
    application_set = tables.Column(verbose_name=_("Application Set"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = ApplicationSetAssignment
        fields = ("pk", "application_set", "assigned_object")
        exclude = ("id",)


class ApplicationSetVirtualDeviceContextAssignmentTable(NetBoxTable):
    assigned_object_parent = tables.Column(
        accessor=tables.A("assigned_object__device"),
        linkify=True,
        orderable=False,
        verbose_name=_("Parent"),
    )
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Virtual Device Context"),
    )
    application_set = tables.Column(verbose_name=_("Application Set"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = ApplicationSetAssignment
        fields = ("pk", "application_set", "assigned_object", "assigned_object_parent")
        exclude = ("id",)
