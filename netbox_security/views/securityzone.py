from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.db.models import Count

from netbox.views import generic
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
    "SecurityZoneAssignmentEditView",
    "SecurityZoneAssignmentDeleteView",
)


@register_model_view(SecurityZone)
class SecurityZoneView(generic.ObjectView):
    queryset = SecurityZone.objects.annotate(
        source_policy_count=Count("source_zone_policies"),
        destination_policy_count=Count("destination_zone_policies"),
    )
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


@register_model_view(SecurityZone, "list", path="", detail=False)
class SecurityZoneListView(generic.ObjectListView):
    queryset = SecurityZone.objects.annotate(
        source_policy_count=Count("source_zone_policies"),
        destination_policy_count=Count("destination_zone_policies"),
    )
    filterset = SecurityZoneFilterSet
    filterset_form = SecurityZoneFilterForm
    table = SecurityZoneTable


@register_model_view(SecurityZone, "add", detail=False)
@register_model_view(SecurityZone, "edit")
class SecurityZoneEditView(generic.ObjectEditView):
    queryset = SecurityZone.objects.all()
    form = SecurityZoneForm


@register_model_view(SecurityZone, "delete")
class SecurityZoneDeleteView(generic.ObjectDeleteView):
    queryset = SecurityZone.objects.all()


@register_model_view(SecurityZone, "bulk_edit", path="edit", detail=False)
class SecurityZoneBulkEditView(generic.BulkEditView):
    queryset = SecurityZone.objects.all()
    filterset = SecurityZoneFilterSet
    table = SecurityZoneTable
    form = SecurityZoneBulkEditForm


@register_model_view(SecurityZone, "bulk_delete", path="delete", detail=False)
class SecurityZoneBulkDeleteView(generic.BulkDeleteView):
    queryset = SecurityZone.objects.all()
    table = SecurityZoneTable


@register_model_view(SecurityZone, "bulk_import", detail=False)
class SecurityZoneBulkImportView(generic.BulkImportView):
    queryset = SecurityZone.objects.all()
    model_form = SecurityZoneImportForm


@register_model_view(SecurityZoneAssignment, "add", detail=False)
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
