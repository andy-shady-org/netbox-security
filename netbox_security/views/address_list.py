from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from utilities.views import register_model_view

from netbox_security.models import AddressList, AddressListAssignment
from netbox_security.forms import (
    AddressListForm,
    AddressListAssignmentForm,
)


__all__ = (
    "AddressListEditView",
    "AddressListDeleteView",
    "AddressListAssignmentEditView",
    "AddressListAssignmentDeleteView",
)


@register_model_view(AddressList, "add", detail=False)
@register_model_view(AddressList, "edit")
class AddressListEditView(generic.ObjectEditView):
    queryset = AddressList.objects.all()
    form = AddressListForm

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


@register_model_view(AddressList, "delete")
class AddressListDeleteView(generic.ObjectDeleteView):
    queryset = AddressList.objects.all()


@register_model_view(AddressListAssignment, "add", detail=False)
@register_model_view(AddressListAssignment, "edit")
class AddressListAssignmentEditView(generic.ObjectEditView):
    queryset = AddressListAssignment.objects.all()
    form = AddressListAssignmentForm

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


@register_model_view(AddressListAssignment, "delete")
class AddressListAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = AddressListAssignment.objects.all()
