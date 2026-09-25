from netbox.views import generic
from utilities.views import register_model_view
from netbox.object_actions import BulkExport

from netbox_security.utils.assignment import get_assigned_object
from netbox_security.constants import ADDRESS_ASSIGNMENT_MODELS

from netbox_security.models import AddressList, AddressListAssignment
from netbox_security.filtersets import (
    AddressListFilterSet,
    AddressListAssignmentFilterSet,
)
from netbox_security.tables import (
    AddressListTable,
    AddressListAssignmentTable,
)
from netbox_security.forms import (
    AddressListForm,
    AddressListFilterForm,
    AddressListAssignmentForm,
    AddressListAssignmentFilterForm,
)

__all__ = (
    "AddressListEditView",
    "AddressListDeleteView",
    "AddressListAssignmentListView",
    "AddressListAssignmentEditView",
    "AddressListAssignmentDeleteView",
    "AddressListAssignmentBulkDeleteView",
)


@register_model_view(AddressList, "list", path="", detail=False)
class AddressListView(generic.ObjectListView):
    queryset = AddressList.objects.all()
    filterset = AddressListFilterSet
    filterset_form = AddressListFilterForm
    table = AddressListTable
    actions = ()


@register_model_view(AddressList, "add", detail=False)
@register_model_view(AddressList, "edit")
class AddressListEditView(generic.ObjectEditView):
    queryset = AddressList.objects.all()
    form = AddressListForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if not obj.pk:
            obj.assigned_object = get_assigned_object(
                request,
                allowed_content_type_filter=ADDRESS_LIST_ASSIGNMENT_MODELS,
            )

        return obj

    def get_extra_addanother_params(self, request):
        return {
            "assigned_object_type": request.GET.get("assigned_object_type"),
            "assigned_object_id": request.GET.get("assigned_object_id"),
        }


@register_model_view(AddressList, "delete")
class AddressListDeleteView(generic.ObjectDeleteView):
    queryset = AddressList.objects.all()


@register_model_view(AddressListAssignment, "list", path="", detail=False)
class AddressListAssignmentListView(generic.ObjectListView):
    queryset = AddressListAssignment.objects.all()
    filterset = AddressListAssignmentFilterSet
    filterset_form = AddressListAssignmentFilterForm
    table = AddressListAssignmentTable
    actions = [BulkExport]


@register_model_view(AddressListAssignment, "add", detail=False)
@register_model_view(AddressListAssignment, "edit")
class AddressListAssignmentEditView(generic.ObjectEditView):
    queryset = AddressListAssignment.objects.all()
    form = AddressListAssignmentForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if not obj.pk:
            obj.assigned_object = get_assigned_object(
                request,
                allowed_content_type_filter=ADDRESS_ASSIGNMENT_MODELS,
            )

        return obj

    def get_extra_addanother_params(self, request):
        return {
            "assigned_object_type": request.GET.get("assigned_object_type"),
            "assigned_object_id": request.GET.get("assigned_object_id"),
        }


@register_model_view(AddressListAssignment, "delete")
class AddressListAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = AddressListAssignment.objects.all()


@register_model_view(AddressListAssignment, "bulk_delete", path="delete", detail=False)
class AddressListAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = AddressListAssignment.objects.all()
    table = AddressListAssignmentTable
