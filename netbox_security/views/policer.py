from netbox.views import generic
from utilities.views import register_model_view
from netbox.object_actions import BulkExport

from dcim.models import Device, VirtualDeviceContext
from dcim.tables import DeviceTable, VirtualDeviceContextTable
from virtualization.models import VirtualMachine
from virtualization.tables import VirtualMachineTable

from netbox_security.utils.assignment import get_assigned_object
from netbox_security.constants import POLICER_ASSIGNMENT_MODELS
from netbox_security.tables import PolicerTable, PolicerAssignmentTable
from netbox_security.filtersets import PolicerFilterSet, PolicerAssignmentFilterSet

from netbox_security.models import Policer, PolicerAssignment
from netbox_security.forms import (
    PolicerFilterForm,
    PolicerForm,
    PolicerBulkEditForm,
    PolicerImportForm,
    PolicerAssignmentForm,
    PolicerAssignmentFilterForm,
)

__all__ = (
    "PolicerView",
    "PolicerListView",
    "PolicerEditView",
    "PolicerDeleteView",
    "PolicerBulkEditView",
    "PolicerBulkDeleteView",
    "PolicerBulkImportView",
    "PolicerAssignmentListView",
    "PolicerAssignmentBulkDeleteView",
)


@register_model_view(Policer)
class PolicerView(generic.ObjectView):
    queryset = Policer.objects.all()
    template_name = "netbox_security/policer.html"

    def get_extra_context(self, request, instance):
        table_definitions = {
            "device_assignments_table": (
                DeviceTable,
                Device.objects.restrict(request.user, "view").filter(
                    policers__policer=instance
                ),
            ),
            "virtual_device_assignments_table": (
                VirtualDeviceContextTable,
                VirtualDeviceContext.objects.restrict(request.user, "view").filter(
                    policers__policer=instance
                ),
            ),
            "virtual_machine_assignments_table": (
                VirtualMachineTable,
                VirtualMachine.objects.restrict(request.user, "view").filter(
                    policers__policer=instance
                ),
            ),
        }
        context = {}
        for name, (table_class, queryset) in table_definitions.items():
            table = table_class(queryset, orderable=False)
            table.configure(request)
            context[name] = table

        return context


@register_model_view(Policer, "list", path="", detail=False)
class PolicerListView(generic.ObjectListView):
    queryset = Policer.objects.all()
    filterset = PolicerFilterSet
    filterset_form = PolicerFilterForm
    table = PolicerTable


@register_model_view(Policer, "add", detail=False)
@register_model_view(Policer, "edit")
class PolicerEditView(generic.ObjectEditView):
    queryset = Policer.objects.all()
    form = PolicerForm


@register_model_view(Policer, "delete")
class PolicerDeleteView(generic.ObjectDeleteView):
    queryset = Policer.objects.all()


@register_model_view(Policer, "bulk_edit", path="edit", detail=False)
class PolicerBulkEditView(generic.BulkEditView):
    queryset = Policer.objects.all()
    filterset = PolicerFilterSet
    table = PolicerTable
    form = PolicerBulkEditForm


@register_model_view(Policer, "bulk_delete", path="delete", detail=False)
class PolicerBulkDeleteView(generic.BulkDeleteView):
    queryset = Policer.objects.all()
    table = PolicerTable


@register_model_view(Policer, "bulk_import", detail=False)
class PolicerBulkImportView(generic.BulkImportView):
    queryset = Policer.objects.all()
    model_form = PolicerImportForm


@register_model_view(PolicerAssignment, "list", path="", detail=False)
class PolicerAssignmentListView(generic.ObjectListView):
    queryset = PolicerAssignment.objects.all()
    filterset = PolicerAssignmentFilterSet
    filterset_form = PolicerAssignmentFilterForm
    table = PolicerAssignmentTable
    actions = [BulkExport]


@register_model_view(PolicerAssignment, "add", detail=False)
@register_model_view(PolicerAssignment, "edit")
class PolicerAssignmentEditView(generic.ObjectEditView):
    queryset = PolicerAssignment.objects.all()
    form = PolicerAssignmentForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if not obj.pk:
            obj.assigned_object = get_assigned_object(
                request,
                allowed_content_type_filter=POLICER_ASSIGNMENT_MODELS,
            )

        return obj

    def get_extra_addanother_params(self, request):
        return {
            "assigned_object_type": request.GET.get("assigned_object_type"),
            "assigned_object_id": request.GET.get("assigned_object_id"),
        }


@register_model_view(PolicerAssignment, "delete")
class PolicerAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = PolicerAssignment.objects.all()


@register_model_view(PolicerAssignment, "bulk_delete", path="delete", detail=False)
class PolicerAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = PolicerAssignment.objects.all()
    table = PolicerAssignmentTable
