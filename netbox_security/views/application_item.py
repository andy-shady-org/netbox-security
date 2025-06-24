from netbox.views import generic
from utilities.views import register_model_view

from netbox_security.tables import ApplicationItemTable
from netbox_security.filtersets import ApplicationItemFilterSet

from netbox_security.models import ApplicationItem
from netbox_security.forms import (
    ApplicationItemFilterForm,
    ApplicationItemForm,
    ApplicationItemBulkEditForm,
    ApplicationItemImportForm,
)


__all__ = (
    "ApplicationItemView",
    "ApplicationItemListView",
    "ApplicationItemEditView",
    "ApplicationItemDeleteView",
    "ApplicationItemBulkEditView",
    "ApplicationItemBulkDeleteView",
    "ApplicationItemBulkImportView",
)


@register_model_view(ApplicationItem)
class ApplicationItemView(generic.ObjectView):
    queryset = ApplicationItem.objects.all()
    template_name = "netbox_security/applicationitem.html"


@register_model_view(ApplicationItem, "list", path="", detail=False)
class ApplicationItemListView(generic.ObjectListView):
    queryset = ApplicationItem.objects.all()
    filterset = ApplicationItemFilterSet
    filterset_form = ApplicationItemFilterForm
    table = ApplicationItemTable


@register_model_view(ApplicationItem, "add", detail=False)
@register_model_view(ApplicationItem, "edit")
class ApplicationItemEditView(generic.ObjectEditView):
    queryset = ApplicationItem.objects.all()
    form = ApplicationItemForm


@register_model_view(ApplicationItem, "delete")
class ApplicationItemDeleteView(generic.ObjectDeleteView):
    queryset = ApplicationItem.objects.all()


@register_model_view(ApplicationItem, "bulk_edit", path="edit", detail=False)
class ApplicationItemBulkEditView(generic.BulkEditView):
    queryset = ApplicationItem.objects.all()
    filterset = ApplicationItemFilterSet
    table = ApplicationItemTable
    form = ApplicationItemBulkEditForm


@register_model_view(ApplicationItem, "bulk_delete", path="delete", detail=False)
class ApplicationItemBulkDeleteView(generic.BulkDeleteView):
    queryset = ApplicationItem.objects.all()
    table = ApplicationItemTable


@register_model_view(ApplicationItem, "bulk_import", detail=False)
class ApplicationItemBulkImportView(generic.BulkImportView):
    queryset = ApplicationItem.objects.all()
    model_form = ApplicationItemImportForm
