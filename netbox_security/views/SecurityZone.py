from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from tenancy.views import ObjectContactsView
from utilities.views import register_model_view

from netbox_security.tables import SecurityZoneTable
from netbox_security.filtersets import SecurityZoneFilterSet

from netbox_security.models import SecurityZone, SecurityZoneAssignment
from netbox_security.forms import (
    SecurityZoneFilterForm,
    SecurityZoneForm,
    SecurityZoneBulkEditForm,
    SecurityZoneAssignmentForm,
    SecurityZoneImportForm,
)

from netbox_security.tables import SecurityZonePolicyTable


__all__ = (
    "SecurityZoneView",
    "SecurityZoneListView",
    "SecurityZoneEditView",
    "SecurityZoneDeleteView",
    "SecurityZoneBulkEditView",
    "SecurityZoneBulkDeleteView",
    "SecurityZoneBulkImportView",
    "SecurityZoneContactsView",
    "SecurityZoneAssignmentEditView",
    "SecurityZoneAssignmentDeleteView",
)


class SecurityZoneView(generic.ObjectView):
    queryset = SecurityZone.objects.all()
    template_name = "netbox_security/securityzone.html"

    def get_extra_context(self, request, instance):
        source_zone_table = SecurityZonePolicyTable(
            instance.source_zone_policies.all(), orderable=False
        )
        destination_zone_table = SecurityZonePolicyTable(
            instance.destination_zone_policies.all(), orderable=False
        )
        return {
            "source_zone_table": source_zone_table,
            "destination_zone_table": destination_zone_table,
        }


class SecurityZoneListView(generic.ObjectListView):
    queryset = SecurityZone.objects.all()
    filterset = SecurityZoneFilterSet
    filterset_form = SecurityZoneFilterForm
    table = SecurityZoneTable


class SecurityZoneEditView(generic.ObjectEditView):
    queryset = SecurityZone.objects.all()
    form = SecurityZoneForm


class SecurityZoneDeleteView(generic.ObjectDeleteView):
    queryset = SecurityZone.objects.all()
    default_return_url = "plugins:netbox_security:securityzone_list"


class SecurityZoneBulkEditView(generic.BulkEditView):
    queryset = SecurityZone.objects.all()
    filterset = SecurityZoneFilterSet
    table = SecurityZoneTable
    form = SecurityZoneBulkEditForm


class SecurityZoneBulkDeleteView(generic.BulkDeleteView):
    queryset = SecurityZone.objects.all()
    table = SecurityZoneTable
    default_return_url = "plugins:netbox_security:securityzone_list"


class SecurityZoneBulkImportView(generic.BulkImportView):
    queryset = SecurityZone.objects.all()
    model_form = SecurityZoneImportForm


@register_model_view(SecurityZone, "contacts")
class SecurityZoneContactsView(ObjectContactsView):
    queryset = SecurityZone.objects.all()


@register_model_view(SecurityZoneAssignment, "edit")
class SecurityZoneAssignmentEditView(generic.ObjectEditView):
    queryset = SecurityZoneAssignment.objects.all()
    form = SecurityZoneAssignmentForm

    def alter_object(self, instance, request, args, kwargs):
        if not instance.pk:
            content_type = get_object_or_404(
                ContentType, pk=request.GET.get("assigned_object_type")
            )
            instance.assigned_object = get_object_or_404(
                content_type.model_class(), pk=request.GET.get("assigned_object_id")
            )
        return instance

    def get_extra_addanother_params(self, request):
        return {
            "assigned_object_type": request.GET.get("assigned_object_type"),
            "assigned_object_id": request.GET.get("assigned_object_id"),
        }


@register_model_view(SecurityZoneAssignment, "delete")
class SecurityZoneAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = SecurityZoneAssignment.objects.all()
