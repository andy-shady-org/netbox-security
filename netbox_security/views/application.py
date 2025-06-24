from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from utilities.views import register_model_view

from netbox_security.tables import ApplicationTable, ApplicationItemTable
from netbox_security.filtersets import ApplicationFilterSet

from netbox_security.models import Application, ApplicationAssignment
from netbox_security.forms import (
    ApplicationFilterForm,
    ApplicationForm,
    ApplicationBulkEditForm,
    ApplicationAssignmentForm,
    ApplicationImportForm,
)


__all__ = (
    "ApplicationView",
    "ApplicationListView",
    "ApplicationEditView",
    "ApplicationDeleteView",
    "ApplicationBulkEditView",
    "ApplicationBulkDeleteView",
    "ApplicationBulkImportView",
    "ApplicationAssignmentEditView",
    "ApplicationAssignmentDeleteView",
)


@register_model_view(Application)
class ApplicationView(generic.ObjectView):
    queryset = Application.objects.all()
    template_name = "netbox_security/application.html"

    def get_extra_context(self, request, instance):
        items_table = ApplicationItemTable(
            instance.application_items.all(), orderable=False
        )

        return {
            "items_table": items_table,
        }


@register_model_view(Application, "list", path="", detail=False)
class ApplicationListView(generic.ObjectListView):
    queryset = Application.objects.all()
    filterset = ApplicationFilterSet
    filterset_form = ApplicationFilterForm
    table = ApplicationTable


@register_model_view(Application, "add", detail=False)
@register_model_view(Application, "edit")
class ApplicationEditView(generic.ObjectEditView):
    queryset = Application.objects.all()
    form = ApplicationForm


@register_model_view(Application, "delete")
class ApplicationDeleteView(generic.ObjectDeleteView):
    queryset = Application.objects.all()


@register_model_view(Application, "bulk_edit", path="edit", detail=False)
class ApplicationBulkEditView(generic.BulkEditView):
    queryset = Application.objects.all()
    filterset = ApplicationFilterSet
    table = ApplicationTable
    form = ApplicationBulkEditForm


@register_model_view(Application, "bulk_delete", path="delete", detail=False)
class ApplicationBulkDeleteView(generic.BulkDeleteView):
    queryset = Application.objects.all()
    table = ApplicationTable


@register_model_view(Application, "bulk_import", detail=False)
class ApplicationBulkImportView(generic.BulkImportView):
    queryset = Application.objects.all()
    model_form = ApplicationImportForm


@register_model_view(ApplicationAssignment, "add", detail=False)
@register_model_view(ApplicationAssignment, "edit")
class ApplicationAssignmentEditView(generic.ObjectEditView):
    queryset = ApplicationAssignment.objects.all()
    form = ApplicationAssignmentForm

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


@register_model_view(ApplicationAssignment, "delete")
class ApplicationAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = ApplicationAssignment.objects.all()
