from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from utilities.views import register_model_view
from ipam.tables import PrefixTable, IPAddressTable, IPRangeTable

from netbox_security.models import NatRule, NatRuleAssignment

from netbox_security.forms import (
    NatRuleForm,
    NatRuleFilterForm,
    NatRuleBulkEditForm,
    NatRuleImportForm,
    NatRuleAssignmentForm,
)
from netbox_security.filtersets import NatRuleFilterSet
from netbox_security.tables import (
    NatRuleTable,
)


__all__ = (
    "NatRuleView",
    "NatRuleListView",
    "NatRuleEditView",
    "NatRuleDeleteView",
    "NatRuleBulkEditView",
    "NatRuleBulkDeleteView",
    "NatRuleBulkImportView",
    "NatRuleAssignmentEditView",
    "NatRuleAssignmentDeleteView",
)


@register_model_view(NatRule)
class NatRuleView(generic.ObjectView):
    queryset = NatRule.objects.all()
    template_name = "netbox_security/natrule.html"

    def get_extra_context(self, request, instance):
        source_addresses_table = IPAddressTable(
            instance.source_addresses.all(),
            orderable=False,
            exclude=(
                "created",
                "last_updated",
            ),
        )
        destination_addresses_table = IPAddressTable(
            instance.destination_addresses.all(),
            orderable=False,
            exclude=(
                "created",
                "last_updated",
            ),
        )
        source_prefixes_table = PrefixTable(
            instance.source_prefixes.all(),
            orderable=False,
            exclude=(
                "prefix_flat",
                "vlan_group",
                "utilization",
                "tenant_group",
                "scope",
                "scope_type",
                "depth",
                "mark_utilized",
                "children",
                "created",
                "last_updated",
            ),
        )
        destination_prefixes_table = PrefixTable(
            instance.destination_prefixes.all(),
            orderable=False,
            exclude=(
                "prefix_flat",
                "vlan_group",
                "utilization",
                "tenant_group",
                "scope",
                "scope_type",
                "depth",
                "mark_utilized",
                "children",
                "created",
                "last_updated",
            ),
        )
        source_ranges_table = IPRangeTable(
            instance.source_ranges.all(),
            orderable=False,
            exclude=(
                "created",
                "last_updated",
            ),
        )
        destination_ranges_table = IPRangeTable(
            instance.destination_ranges.all(),
            orderable=False,
            exclude=(
                "created",
                "last_updated",
            ),
        )

        return {
            "source_addresses_table": source_addresses_table,
            "destination_addresses_table": destination_addresses_table,
            "source_prefixes_table": source_prefixes_table,
            "destination_prefixes_table": destination_prefixes_table,
            "source_ranges_table": source_ranges_table,
            "destination_ranges_table": destination_ranges_table,
        }


@register_model_view(NatRule, "list", path="", detail=False)
class NatRuleListView(generic.ObjectListView):
    queryset = NatRule.objects.all()
    filterset = NatRuleFilterSet
    filterset_form = NatRuleFilterForm
    table = NatRuleTable


@register_model_view(NatRule, "add", detail=False)
@register_model_view(NatRule, "edit")
class NatRuleEditView(generic.ObjectEditView):
    queryset = NatRule.objects.all()
    form = NatRuleForm


@register_model_view(NatRule, "delete")
class NatRuleDeleteView(generic.ObjectDeleteView):
    queryset = NatRule.objects.all()


@register_model_view(NatRule, "bulk_edit", path="edit", detail=False)
class NatRuleBulkEditView(generic.BulkEditView):
    queryset = NatRule.objects.all()
    filterset = NatRuleFilterSet
    table = NatRuleTable
    form = NatRuleBulkEditForm


@register_model_view(NatRule, "bulk_import", detail=False)
class NatRuleBulkImportView(generic.BulkImportView):
    queryset = NatRule.objects.all()
    model_form = NatRuleImportForm


@register_model_view(NatRule, "bulk_delete", path="delete", detail=False)
class NatRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = NatRule.objects.all()
    table = NatRuleTable


@register_model_view(NatRuleAssignment, "edit")
@register_model_view(NatRuleAssignment, "add", detail=False)
class NatRuleAssignmentEditView(generic.ObjectEditView):
    queryset = NatRuleAssignment.objects.all()
    form = NatRuleAssignmentForm

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


@register_model_view(NatRuleAssignment, "delete")
class NatRuleAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = NatRuleAssignment.objects.all()
