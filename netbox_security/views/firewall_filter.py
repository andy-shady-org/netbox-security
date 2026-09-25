from django.db.models import Count

from netbox.views import generic
from utilities.views import register_model_view
from netbox.object_actions import BulkExport

from dcim.models import Device, VirtualDeviceContext
from dcim.tables import DeviceTable, VirtualDeviceContextTable
from virtualization.models import VirtualMachine
from virtualization.tables import VirtualMachineTable

from netbox_security.utils.assignment import get_assigned_object
from netbox_security.constants import FILTER_ASSIGNMENT_MODELS
from netbox_security.tables import FirewallFilterTable, FirewallFilterAssignmentTable
from netbox_security.filtersets import (
    FirewallFilterFilterSet,
    FirewallFilterAssignmentFilterSet,
)

from netbox_security.models import (
    FirewallFilter,
    FirewallFilterAssignment,
)
from netbox_security.forms import (
    FirewallFilterFilterForm,
    FirewallFilterForm,
    FirewallFilterBulkEditForm,
    FirewallFilterAssignmentForm,
    FirewallFilterImportForm,
    FirewallFilterAssignmentFilterForm,
)

__all__ = (
    "FirewallFilterView",
    "FirewallFilterListView",
    "FirewallFilterEditView",
    "FirewallFilterDeleteView",
    "FirewallFilterBulkEditView",
    "FirewallFilterBulkDeleteView",
    "FirewallFilterBulkImportView",
    "FirewallFilterAssignmentEditView",
    "FirewallFilterAssignmentDeleteView",
    "FirewallFilterAssignmentListView",
    "FirewallFilterAssignmentBulkDeleteView",
)


@register_model_view(FirewallFilter)
class FirewallFilterView(generic.ObjectView):
    queryset = FirewallFilter.objects.annotate(
        rule_count=Count("firewallfilterrule_rules")
    )
    template_name = "netbox_security/firewallfilter.html"

    def get_extra_context(self, request, instance):
        table_definitions = {
            "device_assignments_table": (
                DeviceTable,
                Device.objects.restrict(request.user, "view").filter(
                    firewall_filter__firewall_filter=instance
                ),
            ),
            "virtual_device_assignments_table": (
                VirtualDeviceContextTable,
                VirtualDeviceContext.objects.restrict(request.user, "view").filter(
                    firewall_filter__firewall_filter=instance
                ),
            ),
            "virtual_machine_assignments_table": (
                VirtualMachineTable,
                VirtualMachine.objects.restrict(request.user, "view").filter(
                    firewall_filter__firewall_filter=instance
                ),
            ),
        }
        context = {}
        for name, (table_class, queryset) in table_definitions.items():
            table = table_class(queryset, orderable=False)
            table.configure(request)
            context[name] = table

        return context


@register_model_view(FirewallFilter, "list", path="", detail=False)
class FirewallFilterListView(generic.ObjectListView):
    queryset = FirewallFilter.objects.annotate(
        rule_count=Count("firewallfilterrule_rules")
    )
    filterset = FirewallFilterFilterSet
    filterset_form = FirewallFilterFilterForm
    table = FirewallFilterTable


@register_model_view(FirewallFilter, "add", detail=False)
@register_model_view(FirewallFilter, "edit")
class FirewallFilterEditView(generic.ObjectEditView):
    queryset = FirewallFilter.objects.all()
    form = FirewallFilterForm


@register_model_view(FirewallFilter, "delete")
class FirewallFilterDeleteView(generic.ObjectDeleteView):
    queryset = FirewallFilter.objects.all()


@register_model_view(FirewallFilter, "bulk_edit", path="edit", detail=False)
class FirewallFilterBulkEditView(generic.BulkEditView):
    queryset = FirewallFilter.objects.all()
    filterset = FirewallFilterFilterSet
    table = FirewallFilterTable
    form = FirewallFilterBulkEditForm


@register_model_view(FirewallFilter, "bulk_delete", path="delete", detail=False)
class FirewallFilterBulkDeleteView(generic.BulkDeleteView):
    queryset = FirewallFilter.objects.all()
    table = FirewallFilterTable


@register_model_view(FirewallFilter, "bulk_import", detail=False)
class FirewallFilterBulkImportView(generic.BulkImportView):
    queryset = FirewallFilter.objects.all()
    model_form = FirewallFilterImportForm


@register_model_view(FirewallFilterAssignment, "list", path="", detail=False)
class FirewallFilterAssignmentListView(generic.ObjectListView):
    queryset = FirewallFilterAssignment.objects.all()
    filterset = FirewallFilterAssignmentFilterSet
    filterset_form = FirewallFilterAssignmentFilterForm
    table = FirewallFilterAssignmentTable
    actions = [BulkExport]


@register_model_view(FirewallFilterAssignment, "add", detail=False)
@register_model_view(FirewallFilterAssignment, "edit")
class FirewallFilterAssignmentEditView(generic.ObjectEditView):
    queryset = FirewallFilterAssignment.objects.all()
    form = FirewallFilterAssignmentForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if not obj.pk:
            obj.assigned_object = get_assigned_object(
                request,
                allowed_content_type_filter=FILTER_ASSIGNMENT_MODELS,
            )

        return obj

    def get_extra_addanother_params(self, request):
        return {
            "assigned_object_type": request.GET.get("assigned_object_type"),
            "assigned_object_id": request.GET.get("assigned_object_id"),
        }


@register_model_view(FirewallFilterAssignment, "delete")
class FirewallFilterAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = FirewallFilterAssignment.objects.all()


@register_model_view(
    FirewallFilterAssignment, "bulk_delete", path="delete", detail=False
)
class FirewallFilterAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = FirewallFilterAssignment.objects.all()
    table = FirewallFilterAssignmentTable
