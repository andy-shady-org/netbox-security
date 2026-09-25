from netbox.views import generic
from utilities.views import register_model_view
from netbox.object_actions import BulkExport

from dcim.models import Device, VirtualDeviceContext
from dcim.tables import DeviceTable, VirtualDeviceContextTable
from virtualization.models import VirtualMachine
from virtualization.tables import VirtualMachineTable

from netbox_security.utils.assignment import get_assigned_object
from netbox_security.constants import APPLICATION_ASSIGNMENT_MODELS
from netbox_security.tables import ApplicationSetTable, ApplicationSetAssignmentTable
from netbox_security.filtersets import (
    ApplicationSetFilterSet,
    ApplicationSetAssignmentFilterSet,
)

from netbox_security.models import ApplicationSet, ApplicationSetAssignment
from netbox_security.forms import (
    ApplicationSetFilterForm,
    ApplicationSetForm,
    ApplicationSetBulkEditForm,
    ApplicationSetAssignmentForm,
    ApplicationSetImportForm,
    ApplicationSetAssignmentFilterForm,
)

__all__ = (
    "ApplicationSetView",
    "ApplicationSetListView",
    "ApplicationSetEditView",
    "ApplicationSetDeleteView",
    "ApplicationSetBulkEditView",
    "ApplicationSetBulkDeleteView",
    "ApplicationSetBulkImportView",
    "ApplicationSetAssignmentEditView",
    "ApplicationSetAssignmentDeleteView",
    "ApplicationSetAssignmentListView",
    "ApplicationSetAssignmentBulkDeleteView",
)


@register_model_view(ApplicationSet)
class ApplicationSetView(generic.ObjectView):
    queryset = ApplicationSet.objects.all()
    template_name = "netbox_security/applicationset.html"

    def get_extra_context(self, request, instance):
        table_definitions = {
            "device_assignments_table": (
                DeviceTable,
                Device.objects.restrict(request.user, "view").filter(
                    application_sets__application_set=instance
                ),
            ),
            "virtual_device_assignments_table": (
                VirtualDeviceContextTable,
                VirtualDeviceContext.objects.restrict(request.user, "view").filter(
                    application_sets__application_set=instance
                ),
            ),
            "virtual_machine_assignments_table": (
                VirtualMachineTable,
                VirtualMachine.objects.restrict(request.user, "view").filter(
                    application_sets__application_set=instance
                ),
            ),
        }
        context = {}
        for name, (table_class, queryset) in table_definitions.items():
            table = table_class(queryset, orderable=False)
            table.configure(request)
            context[name] = table

        return context


@register_model_view(ApplicationSet, "list", path="", detail=False)
class ApplicationSetListView(generic.ObjectListView):
    queryset = ApplicationSet.objects.all()
    filterset = ApplicationSetFilterSet
    filterset_form = ApplicationSetFilterForm
    table = ApplicationSetTable


@register_model_view(ApplicationSet, "add", detail=False)
@register_model_view(ApplicationSet, "edit")
class ApplicationSetEditView(generic.ObjectEditView):
    queryset = ApplicationSet.objects.all()
    form = ApplicationSetForm


@register_model_view(ApplicationSet, "delete")
class ApplicationSetDeleteView(generic.ObjectDeleteView):
    queryset = ApplicationSet.objects.all()


@register_model_view(ApplicationSet, "bulk_edit", path="edit", detail=False)
class ApplicationSetBulkEditView(generic.BulkEditView):
    queryset = ApplicationSet.objects.all()
    filterset = ApplicationSetFilterSet
    table = ApplicationSetTable
    form = ApplicationSetBulkEditForm


@register_model_view(ApplicationSet, "bulk_delete", path="delete", detail=False)
class ApplicationSetBulkDeleteView(generic.BulkDeleteView):
    queryset = ApplicationSet.objects.all()
    table = ApplicationSetTable


@register_model_view(ApplicationSet, "bulk_import", detail=False)
class ApplicationSetBulkImportView(generic.BulkImportView):
    queryset = ApplicationSet.objects.all()
    model_form = ApplicationSetImportForm


@register_model_view(ApplicationSetAssignment, "list", path="", detail=False)
class ApplicationSetAssignmentListView(generic.ObjectListView):
    queryset = ApplicationSetAssignment.objects.all()
    filterset = ApplicationSetAssignmentFilterSet
    filterset_form = ApplicationSetAssignmentFilterForm
    table = ApplicationSetAssignmentTable
    actions = [BulkExport]


@register_model_view(ApplicationSetAssignment, "add", detail=False)
@register_model_view(ApplicationSetAssignment, "edit")
class ApplicationSetAssignmentEditView(generic.ObjectEditView):
    queryset = ApplicationSetAssignment.objects.all()
    form = ApplicationSetAssignmentForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if not obj.pk:
            obj.assigned_object = get_assigned_object(
                request,
                allowed_content_type_filter=APPLICATION_ASSIGNMENT_MODELS,
            )

        return obj

    def get_extra_addanother_params(self, request):
        return {
            "assigned_object_type": request.GET.get("assigned_object_type"),
            "assigned_object_id": request.GET.get("assigned_object_id"),
        }


@register_model_view(ApplicationSetAssignment, "delete")
class ApplicationSetAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = ApplicationSetAssignment.objects.all()


@register_model_view(
    ApplicationSetAssignment, "bulk_delete", path="delete", detail=False
)
class ApplicationSetAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = ApplicationSetAssignment.objects.all()
    table = ApplicationSetAssignmentTable
