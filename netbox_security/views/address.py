from netbox.views import generic
from utilities.views import register_model_view
from netbox.object_actions import BulkExport

from dcim.models import Device, VirtualDeviceContext
from dcim.tables import DeviceTable, VirtualDeviceContextTable
from virtualization.models import VirtualMachine
from virtualization.tables import VirtualMachineTable

from netbox_security.utils.assignment import get_assigned_object
from netbox_security.constants import ADDRESS_ASSIGNMENT_MODELS

from netbox_security.tables import (
    AddressTable,
    AddressAssignmentTable,
    SecurityZoneTable,
)
from netbox_security.filtersets import AddressFilterSet, AddressAssignmentFilterSet

from netbox_security.models import Address, AddressAssignment, SecurityZone
from netbox_security.forms import (
    AddressFilterForm,
    AddressForm,
    AddressBulkEditForm,
    AddressAssignmentForm,
    AddressImportForm,
    AddressAssignmentFilterForm,
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
    "AddressAssignmentListView",
    "AddressAssignmentBulkDeleteView",
)


@register_model_view(Address)
class AddressView(generic.ObjectView):
    queryset = Address.objects.all()
    template_name = "netbox_security/address.html"

    def get_extra_context(self, request, instance):
        table_definitions = {
            "device_assignments_table": (
                DeviceTable,
                Device.objects.restrict(request.user, "view").filter(
                    addresses__address=instance
                ),
            ),
            "virtual_device_assignments_table": (
                VirtualDeviceContextTable,
                VirtualDeviceContext.objects.restrict(request.user, "view").filter(
                    addresses__address=instance
                ),
            ),
            "virtual_machine_assignments_table": (
                VirtualMachineTable,
                VirtualMachine.objects.restrict(request.user, "view").filter(
                    addresses__address=instance
                ),
            ),
            "zone_assignments_table": (
                SecurityZoneTable,
                SecurityZone.objects.restrict(request.user, "view").filter(
                    addresses__address=instance
                ),
            ),
        }
        context = {}
        for name, (table_class, queryset) in table_definitions.items():
            table = table_class(queryset, orderable=False)
            table.configure(request)
            context[name] = table

        return context


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


@register_model_view(AddressAssignment, "list", path="", detail=False)
class AddressAssignmentListView(generic.ObjectListView):
    queryset = AddressAssignment.objects.all()
    filterset = AddressAssignmentFilterSet
    filterset_form = AddressAssignmentFilterForm
    table = AddressAssignmentTable
    actions = [BulkExport]


@register_model_view(AddressAssignment, "add", detail=False)
@register_model_view(AddressAssignment, "edit")
class AddressAssignmentEditView(generic.ObjectEditView):
    queryset = AddressAssignment.objects.all()
    form = AddressAssignmentForm

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


@register_model_view(AddressAssignment, "delete")
class AddressAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = AddressAssignment.objects.all()


@register_model_view(AddressAssignment, "bulk_delete", path="delete", detail=False)
class AddressAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = AddressAssignment.objects.all()
    table = AddressAssignmentTable
