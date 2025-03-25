from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from tenancy.views import ObjectContactsView
from utilities.views import register_model_view

from netbox_security.tables import AddressListTable
from netbox_security.filtersets import AddressListFilterSet

from netbox_security.models import (
    AddressList,
    AddressListAssignment
)
from netbox_security.forms import (
    AddressListFilterForm,
    AddressListForm,
    AddressListBulkEditForm,
    AddressListAssignmentForm,
    AddressListImportForm
)


__all__ = (
    'AddressListView',
    'AddressListListView',
    'AddressListEditView',
    'AddressListDeleteView',
    'AddressListBulkEditView',
    'AddressListBulkDeleteView',
    'AddressListBulkImportView',
    'AddressListContactsView',
    'AddressListAssignmentEditView',
    'AddressListAssignmentDeleteView',
)


class AddressListView(generic.ObjectView):
    queryset = AddressList.objects.all()
    template_name = 'netbox_security/addresslist.html'


class AddressListListView(generic.ObjectListView):
    queryset = AddressList.objects.all()
    filterset = AddressListFilterSet
    filterset_form = AddressListFilterForm
    table = AddressListTable


class AddressListEditView(generic.ObjectEditView):
    queryset = AddressList.objects.all()
    form = AddressListForm


class AddressListDeleteView(generic.ObjectDeleteView):
    queryset = AddressList.objects.all()
    default_return_url = 'plugins:netbox_security:addresslist_list'


class AddressListBulkEditView(generic.BulkEditView):
    queryset = AddressList.objects.all()
    filterset = AddressListFilterSet
    table = AddressListTable
    form = AddressListBulkEditForm


class AddressListBulkDeleteView(generic.BulkDeleteView):
    queryset = AddressList.objects.all()
    table = AddressListTable
    default_return_url = 'plugins:netbox_security:addresslist_list'


class AddressListBulkImportView(generic.BulkImportView):
    queryset = AddressList.objects.all()
    model_form = AddressListImportForm


@register_model_view(AddressList, "contacts")
class AddressListContactsView(ObjectContactsView):
    queryset = AddressList.objects.all()


@register_model_view(AddressListAssignment, 'edit')
class AddressListAssignmentEditView(generic.ObjectEditView):
    queryset = AddressListAssignment.objects.all()
    form = AddressListAssignmentForm

    def alter_object(self, instance, request, args, kwargs):
        if not instance.pk:
            content_type = get_object_or_404(ContentType, pk=request.GET.get('assigned_object_type'))
            instance.assigned_object = get_object_or_404(content_type.model_class(), pk=request.GET.get('assigned_object_id'))
        return instance

    def get_extra_addanother_params(self, request):
        return {
            'assigned_object_type': request.GET.get('assigned_object_type'),
            'assigned_object_id': request.GET.get('assigned_object_id'),
        }


@register_model_view(AddressListAssignment, 'delete')
class AddressListAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = AddressListAssignment.objects.all()
