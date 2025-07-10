from netbox.views import generic
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from utilities.views import register_model_view, ViewTab

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
)


@register_model_view(NatRuleSet)
class NatRuleSetView(generic.ObjectView):
    queryset = NatRuleSet.objects.annotate(rule_count=Count("natrule_rules"))
    template_name = "netbox_security/natruleset.html"


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
        badge=lambda obj: obj.natrule_rules.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.natrule_rules


@register_model_view(NatRuleSetAssignment, "list", path="", detail=False)
class NatRuleSetAssignmentListView(generic.ObjectListView):
    queryset = NatRuleSetAssignment.objects.all()
    filterset = NatRuleSetAssignmentFilterSet
    filterset_form = NatRuleSetAssignmentFilterForm
    table = NatRuleSetAssignmentTable


@register_model_view(NatRuleSetAssignment, "add", detail=False)
@register_model_view(NatRuleSetAssignment, "edit")
class NatRuleSetAssignmentEditView(generic.ObjectEditView):
    queryset = NatRuleSetAssignment.objects.all()
    form = NatRuleSetAssignmentForm

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


@register_model_view(NatRuleSetAssignment, "delete")
class NatRuleSetAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = NatRuleSetAssignment.objects.all()
