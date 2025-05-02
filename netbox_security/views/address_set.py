from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from utilities.views import register_model_view

from netbox_security.tables import AddressSetTable, AddressTable
from netbox_security.filtersets import AddressSetFilterSet

from netbox_security.models import AddressSet, AddressSetAssignment
from netbox_security.forms import (
    AddressSetFilterForm,
    AddressSetForm,
    AddressSetBulkEditForm,
    AddressSetAssignmentForm,
    AddressSetImportForm,
)


__all__ = (
    "AddressSetView",
    "AddressSetListView",
    "AddressSetEditView",
    "AddressSetDeleteView",
    "AddressSetBulkEditView",
    "AddressSetBulkDeleteView",
    "AddressSetBulkImportView",
    "AddressSetAssignmentEditView",
    "AddressSetAssignmentDeleteView",
)


@register_model_view(AddressSet)
class AddressSetView(generic.ObjectView):
    queryset = AddressSet.objects.all()
    template_name = "netbox_security/addressset.html"

    def get_extra_context(self, request, instance):
        address_table = AddressTable(instance.addresses.all(), orderable=False)
        return {
            "address_table": address_table,
        }


@register_model_view(AddressSet, "list", path="", detail=False)
class AddressSetListView(generic.ObjectListView):
    queryset = AddressSet.objects.all()
    filterset = AddressSetFilterSet
    filterset_form = AddressSetFilterForm
    table = AddressSetTable


@register_model_view(AddressSet, "add", detail=False)
@register_model_view(AddressSet, "edit")
class AddressSetEditView(generic.ObjectEditView):
    queryset = AddressSet.objects.all()
    form = AddressSetForm


@register_model_view(AddressSet, "delete")
class AddressSetDeleteView(generic.ObjectDeleteView):
    queryset = AddressSet.objects.all()


@register_model_view(AddressSet, "bulk_edit", path="edit", detail=False)
class AddressSetBulkEditView(generic.BulkEditView):
    queryset = AddressSet.objects.all()
    filterset = AddressSetFilterSet
    table = AddressSetTable
    form = AddressSetBulkEditForm


@register_model_view(AddressSet, "bulk_delete", path="delete", detail=False)
class AddressSetBulkDeleteView(generic.BulkDeleteView):
    queryset = AddressSet.objects.all()
    table = AddressSetTable


@register_model_view(AddressSet, "bulk_import", detail=False)
class AddressSetBulkImportView(generic.BulkImportView):
    queryset = AddressSet.objects.all()
    model_form = AddressSetImportForm


@register_model_view(AddressSetAssignment, "add", detail=False)
@register_model_view(AddressSetAssignment, "edit")
class AddressSetAssignmentEditView(generic.ObjectEditView):
    queryset = AddressSetAssignment.objects.all()
    form = AddressSetAssignmentForm

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


@register_model_view(AddressSetAssignment, "delete")
class AddressSetAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = AddressSetAssignment.objects.all()
