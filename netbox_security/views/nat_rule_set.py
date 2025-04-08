from netbox.views import generic
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from utilities.views import register_model_view, ViewTab
from tenancy.views import ObjectContactsView

from netbox_security.models import NatRuleSet, NatRuleSetAssignment, NatRule
from netbox_security.tables import NatRuleSetTable, NatRuleTable, SecurityZoneTable
from netbox_security.filtersets import NatRuleSetFilterSet, NatRuleFilterSet
from netbox_security.forms import (
    NatRuleSetFilterForm,
    NatRuleSetForm,
    NatRuleSetBulkEditForm,
    NatRuleSetImportForm,
    NatRuleSetAssignmentForm,
)


__all__ = (
    "NatRuleSetView",
    "NatRuleSetListView",
    "NatRuleSetEditView",
    "NatRuleSetDeleteView",
    "NatRuleSetBulkEditView",
    "NatRuleSetBulkImportView",
    "NatRuleSetBulkDeleteView",
    "NatRuleSetContactsView",
    "NatRuleSetRulesView",
    "NatRuleSetAssignmentEditView",
    "NatRuleSetAssignmentDeleteView",
)


@register_model_view(NatRuleSet)
class NatRuleSetView(generic.ObjectView):
    queryset = NatRuleSet.objects.all()
    template_name = "netbox_security/natruleset.html"

    def get_extra_context(self, request, instance):
        source_zones_qs = instance.source_zones.all()
        destination_zones_qs = instance.destination_zones.all()
        source_zones_table = SecurityZoneTable(source_zones_qs, orderable=False)
        destination_zones_table = SecurityZoneTable(
            destination_zones_qs, orderable=False
        )
        return {
            "source_zones_table": source_zones_table,
            "destination_zones_table": destination_zones_table,
        }


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
    default_return_url = "plugins:netbox_security:natruleset_list"


@register_model_view(NatRuleSet, "contacts")
class NatRuleSetContactsView(ObjectContactsView):
    queryset = NatRuleSet.objects.all()


@register_model_view(NatRuleSet, name="rules")
class NatRuleSetRulesView(generic.ObjectChildrenView):
    template_name = "netbox_security/natruleset_rules.html"
    queryset = NatRuleSet.objects.all()
    child_model = NatRule
    table = NatRuleTable
    filterset = NatRuleFilterSet
    actions = []
    tab = ViewTab(
        label=_("NAT Rules"),
        badge=lambda obj: NatRule.objects.filter(rule_set=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(rule_set=parent)


@register_model_view(NatRuleSetAssignment, "add")
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
