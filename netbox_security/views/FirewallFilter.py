from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from tenancy.views import ObjectContactsView
from utilities.views import register_model_view

from netbox_security.tables import FirewallFilterTable
from netbox_security.filtersets import FirewallFilterFilterSet

from netbox_security.models import (
    FirewallFilter,
    FirewallFilterAssignment
)
from netbox_security.forms import (
    FirewallFilterFilterForm,
    FirewallFilterForm,
    FirewallFilterBulkEditForm,
    FirewallFilterAssignmentForm,
    FirewallFilterImportForm
)


__all__ = (
    'FirewallFilterView',
    'FirewallFilterListView',
    'FirewallFilterEditView',
    'FirewallFilterDeleteView',
    'FirewallFilterBulkEditView',
    'FirewallFilterBulkDeleteView',
    'FirewallFilterBulkImportView',
    'FirewallFilterContactsView',
    'FirewallFilterAssignmentEditView',
    'FirewallFilterAssignmentDeleteView',
)


class FirewallFilterView(generic.ObjectView):
    queryset = FirewallFilter.objects.all()
    template_name = 'netbox_security/firewallfilter.html'


class FirewallFilterListView(generic.ObjectListView):
    queryset = FirewallFilter.objects.all()
    filterset = FirewallFilterFilterSet
    filterset_form = FirewallFilterFilterForm
    table = FirewallFilterTable


class FirewallFilterEditView(generic.ObjectEditView):
    queryset = FirewallFilter.objects.all()
    form = FirewallFilterForm


class FirewallFilterDeleteView(generic.ObjectDeleteView):
    queryset = FirewallFilter.objects.all()
    default_return_url = 'plugins:netbox_security:firewallfilter_list'


class FirewallFilterBulkEditView(generic.BulkEditView):
    queryset = FirewallFilter.objects.all()
    filterset = FirewallFilterFilterSet
    table = FirewallFilterTable
    form = FirewallFilterBulkEditForm


class FirewallFilterBulkDeleteView(generic.BulkDeleteView):
    queryset = FirewallFilter.objects.all()
    table = FirewallFilterTable
    default_return_url = 'plugins:netbox_security:firewallfilter_list'


class FirewallFilterBulkImportView(generic.BulkImportView):
    queryset = FirewallFilter.objects.all()
    model_form = FirewallFilterImportForm


@register_model_view(FirewallFilter, "contacts")
class FirewallFilterContactsView(ObjectContactsView):
    queryset = FirewallFilter.objects.all()


@register_model_view(FirewallFilterAssignment, 'edit')
class FirewallFilterAssignmentEditView(generic.ObjectEditView):
    queryset = FirewallFilterAssignment.objects.all()
    form = FirewallFilterAssignmentForm

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


@register_model_view(FirewallFilterAssignment, 'delete')
class FirewallFilterAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = FirewallFilterAssignment.objects.all()
