from netbox.views import generic
from utilities.views import register_model_view
from netbox.object_actions import BulkExport

from dcim.models import Device, VirtualDeviceContext
from virtualization.models import VirtualMachine

from dcim.tables import DeviceTable, VirtualDeviceContextTable
from dcim.models import Interface

from dcim.tables import InterfaceTable
from virtualization.tables import VirtualMachineTable

from netbox_security.utils.assignment import get_assigned_object
from netbox_security.constants import ZONE_ASSIGNMENT_MODELS
from netbox_security.tables import SecurityZoneTable, SecurityZoneAssignmentTable
from netbox_security.filtersets import (
    SecurityZoneFilterSet,
    SecurityZoneAssignmentFilterSet,
)

from netbox_security.models import SecurityZone, SecurityZoneAssignment
from netbox_security.forms import (
    SecurityZoneFilterForm,
    SecurityZoneForm,
    SecurityZoneBulkEditForm,
    SecurityZoneAssignmentForm,
    SecurityZoneImportForm,
    SecurityZoneAssignmentFilterForm,
)

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
    "SecurityZoneAssignmentListView",
    "SecurityZoneAssignmentBulkDeleteView",
)


@register_model_view(SecurityZone)
class SecurityZoneView(generic.ObjectView):
    queryset = SecurityZone.objects.all()
    template_name = "netbox_security/securityzone.html"

    def get_queryset(self, request):
        return SecurityZone.annotated_queryset(
            user=request.user, queryset=super().get_queryset(request)
        )

    def get_extra_context(self, request, instance):
        table_definitions = {
            "device_assignments_table": (
                DeviceTable,
                Device.objects.restrict(request.user, "view").filter(
                    security_zones__zone=instance
                ),
            ),
            "virtual_device_assignments_table": (
                VirtualDeviceContextTable,
                VirtualDeviceContext.objects.restrict(request.user, "view").filter(
                    security_zones__zone=instance
                ),
            ),
            "virtual_machine_assignments_table": (
                VirtualMachineTable,
                VirtualMachine.objects.restrict(request.user, "view").filter(
                    security_zones__zone=instance
                ),
            ),
            "interface_assignments_table": (
                InterfaceTable,
                Interface.objects.restrict(request.user, "view").filter(
                    security_zones__zone=instance
                ),
            ),
        }

        context = {}
        for name, (table_class, queryset) in table_definitions.items():
            table = table_class(queryset, orderable=False)
            table.configure(request)
            context[name] = table

        return context


@register_model_view(SecurityZone, "list", path="", detail=False)
class SecurityZoneListView(generic.ObjectListView):
    queryset = SecurityZone.objects.all()
    filterset = SecurityZoneFilterSet
    filterset_form = SecurityZoneFilterForm
    table = SecurityZoneTable

    def get_queryset(self, request):
        return SecurityZone.annotated_queryset(
            user=request.user, queryset=super().get_queryset(request)
        )


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


@register_model_view(SecurityZoneAssignment, "list", path="", detail=False)
class SecurityZoneAssignmentListView(generic.ObjectListView):
    queryset = SecurityZoneAssignment.objects.all()
    filterset = SecurityZoneAssignmentFilterSet
    filterset_form = SecurityZoneAssignmentFilterForm
    table = SecurityZoneAssignmentTable
    actions = [BulkExport]


@register_model_view(SecurityZoneAssignment, "add", detail=False)
@register_model_view(SecurityZoneAssignment, "edit")
class SecurityZoneAssignmentEditView(generic.ObjectEditView):
    queryset = SecurityZoneAssignment.objects.all()
    form = SecurityZoneAssignmentForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if not obj.pk:
            obj.assigned_object = get_assigned_object(
                request,
                allowed_content_type_filter=ZONE_ASSIGNMENT_MODELS,
            )

        return obj

    def get_extra_addanother_params(self, request):
        return {
            "assigned_object_type": request.GET.get("assigned_object_type"),
            "assigned_object_id": request.GET.get("assigned_object_id"),
        }


@register_model_view(SecurityZoneAssignment, "delete")
class SecurityZoneAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = SecurityZoneAssignment.objects.all()


@register_model_view(SecurityZoneAssignment, "bulk_delete", path="delete", detail=False)
class SecurityZoneAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = SecurityZoneAssignment.objects.all()
    table = SecurityZoneAssignmentTable
