from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from utilities.views import register_model_view

from netbox_security.tables import AddressTable
from netbox_security.filtersets import AddressFilterSet

from netbox_security.models import Address, AddressAssignment
from netbox_security.forms import (
    AddressFilterForm,
    AddressForm,
    AddressBulkEditForm,
    AddressAssignmentForm,
    AddressImportForm,
)


__all__ = (
    "AddressView",
    "AddressListView",
    "AddressEditView",
    "AddressDeleteView",
    "AddressBulkEditView",
    "AddressBulkDeleteView",
    "AddressBulkImportView",
    "AddressAssignmentEditView",
    "AddressAssignmentDeleteView",
)


@register_model_view(Address)
class AddressView(generic.ObjectView):
    queryset = Address.objects.all()
    template_name = "netbox_security/address.html"


@register_model_view(Address, "list", path="", detail=False)
class AddressListView(generic.ObjectListView):
    queryset = Address.objects.all()
    filterset = AddressFilterSet
    filterset_form = AddressFilterForm
    table = AddressTable


@register_model_view(Address, "add", detail=False)
@register_model_view(Address, "edit")
class AddressEditView(generic.ObjectEditView):
    queryset = Address.objects.all()
    form = AddressForm


@register_model_view(Address, "delete")
class AddressDeleteView(generic.ObjectDeleteView):
    queryset = Address.objects.all()


@register_model_view(Address, "bulk_edit", path="edit", detail=False)
class AddressBulkEditView(generic.BulkEditView):
    queryset = Address.objects.all()
    filterset = AddressFilterSet
    table = AddressTable
    form = AddressBulkEditForm


@register_model_view(Address, "bulk_delete", path="delete", detail=False)
class AddressBulkDeleteView(generic.BulkDeleteView):
    queryset = Address.objects.all()
    table = AddressTable


@register_model_view(Address, "bulk_import", detail=False)
class AddressBulkImportView(generic.BulkImportView):
    queryset = Address.objects.all()
    model_form = AddressImportForm


@register_model_view(AddressAssignment, "add", detail=False)
@register_model_view(AddressAssignment, "edit")
class AddressAssignmentEditView(generic.ObjectEditView):
    queryset = AddressAssignment.objects.all()
    form = AddressAssignmentForm

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


@register_model_view(AddressAssignment, "delete")
class AddressAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = AddressAssignment.objects.all()
