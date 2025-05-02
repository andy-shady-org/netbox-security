from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.db.models import Count

from netbox.views import generic
from utilities.views import register_model_view

from netbox_security.tables import FirewallFilterTable
from netbox_security.filtersets import FirewallFilterFilterSet

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
)

from netbox_security.tables import FirewallFilterRuleTable


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
)


@register_model_view(FirewallFilter)
class FirewallFilterView(generic.ObjectView):
    queryset = FirewallFilter.objects.annotate(
        rule_count=Count("firewallfilterrule_rules")
    )
    template_name = "netbox_security/firewallfilter.html"

    def get_extra_context(self, request, instance):
        filter_rules_table = FirewallFilterRuleTable(
            instance.firewallfilterrule_rules.all(), orderable=False
        )
        return {
            "filter_rules_table": filter_rules_table,
        }


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


@register_model_view(FirewallFilterAssignment, "add", detail=False)
@register_model_view(FirewallFilterAssignment, "edit")
class FirewallFilterAssignmentEditView(generic.ObjectEditView):
    queryset = FirewallFilterAssignment.objects.all()
    form = FirewallFilterAssignmentForm

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


@register_model_view(FirewallFilterAssignment, "delete")
class FirewallFilterAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = FirewallFilterAssignment.objects.all()
