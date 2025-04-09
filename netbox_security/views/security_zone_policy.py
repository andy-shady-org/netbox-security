from netbox.views import generic
from tenancy.views import ObjectContactsView
from utilities.views import register_model_view

from netbox_security.tables import SecurityZonePolicyTable, AddressListTable
from netbox_security.filtersets import SecurityZonePolicyFilterSet

from netbox_security.models import (
    SecurityZonePolicy,
)
from netbox_security.forms import (
    SecurityZonePolicyFilterForm,
    SecurityZonePolicyForm,
    SecurityZonePolicyBulkEditForm,
    SecurityZonePolicyImportForm,
)


__all__ = (
    "SecurityZonePolicyView",
    "SecurityZonePolicyListView",
    "SecurityZonePolicyEditView",
    "SecurityZonePolicyDeleteView",
    "SecurityZonePolicyBulkEditView",
    "SecurityZonePolicyBulkDeleteView",
    "SecurityZonePolicyBulkImportView",
    "SecurityZonePolicyContactsView",
)


@register_model_view(SecurityZonePolicy)
class SecurityZonePolicyView(generic.ObjectView):
    queryset = SecurityZonePolicy.objects.all()
    template_name = "netbox_security/securityzonepolicy.html"

    def get_extra_context(self, request, instance):
        source_address_table = AddressListTable(
            instance.source_address.all(), orderable=False
        )
        destination_address_table = AddressListTable(
            instance.destination_address.all(), orderable=False
        )
        return {
            "source_address_table": source_address_table,
            "destination_address_table": destination_address_table,
        }


@register_model_view(SecurityZonePolicy, "list", path="", detail=False)
class SecurityZonePolicyListView(generic.ObjectListView):
    queryset = SecurityZonePolicy.objects.all()
    filterset = SecurityZonePolicyFilterSet
    filterset_form = SecurityZonePolicyFilterForm
    table = SecurityZonePolicyTable


@register_model_view(SecurityZonePolicy, "add", detail=False)
@register_model_view(SecurityZonePolicy, "edit")
class SecurityZonePolicyEditView(generic.ObjectEditView):
    queryset = SecurityZonePolicy.objects.all()
    form = SecurityZonePolicyForm


@register_model_view(SecurityZonePolicy, "delete")
class SecurityZonePolicyDeleteView(generic.ObjectDeleteView):
    queryset = SecurityZonePolicy.objects.all()
    default_return_url = "plugins:netbox_security:securityzonepolicy_list"


@register_model_view(SecurityZonePolicy, "bulk_edit", path="edit", detail=False)
class SecurityZonePolicyBulkEditView(generic.BulkEditView):
    queryset = SecurityZonePolicy.objects.all()
    filterset = SecurityZonePolicyFilterSet
    table = SecurityZonePolicyTable
    form = SecurityZonePolicyBulkEditForm


@register_model_view(SecurityZonePolicy, "bulk_delete", path="delete", detail=False)
class SecurityZonePolicyBulkDeleteView(generic.BulkDeleteView):
    queryset = SecurityZonePolicy.objects.all()
    table = SecurityZonePolicyTable
    default_return_url = "plugins:netbox_security:securityzonepolicy_list"


@register_model_view(SecurityZonePolicy, "bulk_import", detail=False)
class SecurityZonePolicyBulkImportView(generic.BulkImportView):
    queryset = SecurityZonePolicy.objects.all()
    model_form = SecurityZonePolicyImportForm


@register_model_view(SecurityZonePolicy, "contacts")
class SecurityZonePolicyContactsView(ObjectContactsView):
    queryset = SecurityZonePolicy.objects.all()
