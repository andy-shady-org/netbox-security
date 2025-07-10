from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from utilities.views import register_model_view

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
)


@register_model_view(ApplicationSet)
class ApplicationSetView(generic.ObjectView):
    queryset = ApplicationSet.objects.all()
    template_name = "netbox_security/applicationset.html"


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


@register_model_view(ApplicationSetAssignment, "add", detail=False)
@register_model_view(ApplicationSetAssignment, "edit")
class ApplicationSetAssignmentEditView(generic.ObjectEditView):
    queryset = ApplicationSetAssignment.objects.all()
    form = ApplicationSetAssignmentForm

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


@register_model_view(ApplicationSetAssignment, "delete")
class ApplicationSetAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = ApplicationSetAssignment.objects.all()
