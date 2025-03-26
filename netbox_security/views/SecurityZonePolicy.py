from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from tenancy.views import ObjectContactsView
from utilities.views import register_model_view

from netbox_security.tables import SecurityZonePolicyTable
from netbox_security.filtersets import SecurityZonePolicyFilterSet

from netbox_security.models import (
    SecurityZonePolicy,
)
from netbox_security.forms import (
    SecurityZonePolicyFilterForm,
    SecurityZonePolicyForm,
    SecurityZonePolicyBulkEditForm,
    SecurityZonePolicyImportForm
)


__all__ = (
    'SecurityZonePolicyView',
    'SecurityZonePolicyListView',
    'SecurityZonePolicyEditView',
    'SecurityZonePolicyDeleteView',
    'SecurityZonePolicyBulkEditView',
    'SecurityZonePolicyBulkDeleteView',
    'SecurityZonePolicyBulkImportView',
    'SecurityZonePolicyContactsView',
)


class SecurityZonePolicyView(generic.ObjectView):
    queryset = SecurityZonePolicy.objects.all()
    template_name = 'netbox_security/securityzonepolicy.html'


class SecurityZonePolicyListView(generic.ObjectListView):
    queryset = SecurityZonePolicy.objects.all()
    filterset = SecurityZonePolicyFilterSet
    filterset_form = SecurityZonePolicyFilterForm
    table = SecurityZonePolicyTable


class SecurityZonePolicyEditView(generic.ObjectEditView):
    queryset = SecurityZonePolicy.objects.all()
    form = SecurityZonePolicyForm


class SecurityZonePolicyDeleteView(generic.ObjectDeleteView):
    queryset = SecurityZonePolicy.objects.all()
    default_return_url = 'plugins:netbox_security:securityzonepolicy_list'


class SecurityZonePolicyBulkEditView(generic.BulkEditView):
    queryset = SecurityZonePolicy.objects.all()
    filterset = SecurityZonePolicyFilterSet
    table = SecurityZonePolicyTable
    form = SecurityZonePolicyBulkEditForm


class SecurityZonePolicyBulkDeleteView(generic.BulkDeleteView):
    queryset = SecurityZonePolicy.objects.all()
    table = SecurityZonePolicyTable
    default_return_url = 'plugins:netbox_security:securityzonepolicy_list'


class SecurityZonePolicyBulkImportView(generic.BulkImportView):
    queryset = SecurityZonePolicy.objects.all()
    model_form = SecurityZonePolicyImportForm


@register_model_view(SecurityZonePolicy, "contacts")
class SecurityZonePolicyContactsView(ObjectContactsView):
    queryset = SecurityZonePolicy.objects.all()
