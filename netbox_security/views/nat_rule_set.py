from django.utils.translation import gettext_lazy as _
from django.db.models import Count

from netbox.context import current_request
from netbox.views import generic
from utilities.views import register_model_view, ViewTab
from netbox.object_actions import BulkExport

from dcim.models import Device, VirtualDeviceContext
from virtualization.models import VirtualMachine

from dcim.tables import DeviceTable, VirtualDeviceContextTable
from virtualization.tables import VirtualMachineTable

from netbox_security.utils.assignment import get_assigned_object
from netbox_security.constants import RULESET_ASSIGNMENT_MODELS

from netbox_security.models import NatRuleSet, NatRuleSetAssignment, NatRule
from netbox_security.tables import (
    NatRuleSetTable,
    NatRuleTable,
    NatRuleSetAssignmentTable,
)
from netbox_security.filtersets import (
    NatRuleSetFilterSet,
    NatRuleFilterSet,
    NatRuleSetAssignmentFilterSet,
)
from netbox_security.forms import (
    NatRuleSetFilterForm,
    NatRuleSetForm,
    NatRuleSetBulkEditForm,
    NatRuleSetImportForm,
    NatRuleSetAssignmentForm,
    NatRuleSetAssignmentFilterForm,
)

__all__ = (
    "NatRuleSetView",
    "NatRuleSetListView",
    "NatRuleSetEditView",
    "NatRuleSetDeleteView",
    "NatRuleSetBulkEditView",
    "NatRuleSetBulkImportView",
    "NatRuleSetBulkDeleteView",
    "NatRuleSetRulesView",
    "NatRuleSetAssignmentEditView",
    "NatRuleSetAssignmentDeleteView",
    "NatRuleSetAssignmentListView",
    "NatRuleSetAssignmentBulkDeleteView",
)


def _natrule_count(obj):
    request = current_request.get()
    if request is None or getattr(request, "user", None) is None:
        return 0
    return obj.natrule_rules.restrict(request.user, "view").count()


@register_model_view(NatRuleSet)
class NatRuleSetView(generic.ObjectView):
    queryset = NatRuleSet.objects.annotate(rule_count=Count("natrule_rules"))
    template_name = "netbox_security/natruleset.html"

    def get_extra_context(self, request, instance):
        table_definitions = {
            "device_assignments_table": (
                DeviceTable,
                Device.objects.restrict(request.user, "view").filter(
                    natrulesets__ruleset=instance
                ),
            ),
            "virtual_device_assignments_table": (
                VirtualDeviceContextTable,
                VirtualDeviceContext.objects.restrict(request.user, "view").filter(
                    natrulesets__ruleset=instance
                ),
            ),
            "virtual_machine_assignments_table": (
                VirtualMachineTable,
                VirtualMachine.objects.restrict(request.user, "view").filter(
                    natrulesets__ruleset=instance
                ),
            ),
        }
        context = {}
        for name, (table_class, queryset) in table_definitions.items():
            table = table_class(queryset, orderable=False)
            table.configure(request)
            context[name] = table

        return context


@register_model_view(NatRuleSet, "list", path="", detail=False)
class NatRuleSetListView(generic.ObjectListView):
    queryset = NatRuleSet.objects.annotate(rule_count=Count("natrule_rules"))
    filterset = NatRuleSetFilterSet
    filterset_form = NatRuleSetFilterForm
    table = NatRuleSetTable


@register_model_view(NatRuleSet, "add", detail=False)
@register_model_view(NatRuleSet, "edit")
class NatRuleSetEditView(generic.ObjectEditView):
    queryset = NatRuleSet.objects.all()
    form = NatRuleSetForm


@register_model_view(NatRuleSet, "bulk_delete", path="delete", detail=False)
class NatRuleSetBulkDeleteView(generic.BulkDeleteView):
    queryset = NatRuleSet.objects.all()
    table = NatRuleSetTable


@register_model_view(NatRuleSet, "bulk_edit", path="edit", detail=False)
class NatRuleSetBulkEditView(generic.BulkEditView):
    queryset = NatRuleSet.objects.all()
    filterset = NatRuleSetFilterSet
    table = NatRuleSetTable
    form = NatRuleSetBulkEditForm


@register_model_view(NatRuleSet, "bulk_import", detail=False)
class NatRuleSetBulkImportView(generic.BulkImportView):
    queryset = NatRuleSet.objects.all()
    model_form = NatRuleSetImportForm


@register_model_view(NatRuleSet, "delete")
class NatRuleSetDeleteView(generic.ObjectDeleteView):
    queryset = NatRuleSet.objects.all()


@register_model_view(NatRuleSet, name="rules")
class NatRuleSetRulesView(generic.ObjectChildrenView):
    template_name = "netbox_security/natruleset_rules.html"
    queryset = NatRuleSet.objects.all().prefetch_related("natrule_rules")
    child_model = NatRule
    table = NatRuleTable
    filterset = NatRuleFilterSet
    tab = ViewTab(
        label=_("NAT Rules"),
        permission="netbox_security.view_natrule",
        badge=lambda obj: _natrule_count(obj),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.natrule_rules.restrict(request.user, "view")


@register_model_view(NatRuleSetAssignment, "list", path="", detail=False)
class NatRuleSetAssignmentListView(generic.ObjectListView):
    queryset = NatRuleSetAssignment.objects.all()
    filterset = NatRuleSetAssignmentFilterSet
    filterset_form = NatRuleSetAssignmentFilterForm
    table = NatRuleSetAssignmentTable
    actions = [BulkExport]


@register_model_view(NatRuleSetAssignment, "add", detail=False)
@register_model_view(NatRuleSetAssignment, "edit")
class NatRuleSetAssignmentEditView(generic.ObjectEditView):
    queryset = NatRuleSetAssignment.objects.all()
    form = NatRuleSetAssignmentForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if not obj.pk:
            obj.assigned_object = get_assigned_object(
                request,
                allowed_content_type_filter=RULESET_ASSIGNMENT_MODELS,
            )

        return obj

    def get_extra_addanother_params(self, request):
        return {
            "assigned_object_type": request.GET.get("assigned_object_type"),
            "assigned_object_id": request.GET.get("assigned_object_id"),
        }


@register_model_view(NatRuleSetAssignment, "delete")
class NatRuleSetAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = NatRuleSetAssignment.objects.all()


@register_model_view(NatRuleSetAssignment, "bulk_delete", path="delete", detail=False)
class NatRuleSetAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = NatRuleSetAssignment.objects.all()
    table = NatRuleSetAssignmentTable
