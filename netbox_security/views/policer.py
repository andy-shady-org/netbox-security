from netbox.views import generic
from utilities.views import register_model_view
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox_security.tables import PolicerTable
from netbox_security.filtersets import PolicerFilterSet

from netbox_security.models import Policer, PolicerAssignment
from netbox_security.forms import (
    PolicerFilterForm,
    PolicerForm,
    PolicerBulkEditForm,
    PolicerImportForm,
    PolicerAssignmentForm,
)


__all__ = (
    "PolicerView",
    "PolicerListView",
    "PolicerEditView",
    "PolicerDeleteView",
    "PolicerBulkEditView",
    "PolicerBulkDeleteView",
    "PolicerBulkImportView",
)


@register_model_view(Policer)
class PolicerView(generic.ObjectView):
    queryset = Policer.objects.all()
    template_name = "netbox_security/policer.html"


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


@register_model_view(PolicerAssignment, "add", detail=False)
@register_model_view(PolicerAssignment, "edit")
class PolicerAssignmentEditView(generic.ObjectEditView):
    queryset = PolicerAssignment.objects.all()
    form = PolicerAssignmentForm

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


@register_model_view(PolicerAssignment, "delete")
class PolicerAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = PolicerAssignment.objects.all()
