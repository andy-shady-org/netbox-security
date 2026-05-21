from netbox.views import generic
from utilities.views import register_model_view

from netbox_security.tables import (
    CustomPrefixTable,
)
from netbox_security.filtersets import CustomPrefixFilterSet

from netbox_security.models import CustomPrefix, Address
from netbox_security.utilities import get_address_set_hierarchy
from netbox_security.forms import (
    CustomPrefixFilterForm,
    CustomPrefixForm,
    CustomPrefixBulkEditForm,
    CustomPrefixImportForm,
)

__all__ = (
    "CustomPrefixView",
    "CustomPrefixListView",
    "CustomPrefixEditView",
    "CustomPrefixDeleteView",
    "CustomPrefixBulkEditView",
    "CustomPrefixBulkDeleteView",
    "CustomPrefixBulkImportView",
)


@register_model_view(CustomPrefix)
class CustomPrefixView(generic.ObjectView):
    queryset = CustomPrefix.objects.all()
    template_name = "netbox_security/customprefix.html"

    def get_extra_context(self, request, instance):
        return {
            "policy_context": get_address_set_hierarchy(
                app_label="netbox_security",
                model="customprefix",
                object_id=instance.pk,
            ),
        }


@register_model_view(CustomPrefix, "list", path="", detail=False)
class CustomPrefixListView(generic.ObjectListView):
    queryset = CustomPrefix.objects.all()
    filterset = CustomPrefixFilterSet
    filterset_form = CustomPrefixFilterForm
    table = CustomPrefixTable


@register_model_view(CustomPrefix, "add", detail=False)
@register_model_view(CustomPrefix, "edit")
class CustomPrefixEditView(generic.ObjectEditView):
    queryset = CustomPrefix.objects.all()
    form = CustomPrefixForm


@register_model_view(CustomPrefix, "delete")
class CustomPrefixDeleteView(generic.ObjectDeleteView):
    queryset = CustomPrefix.objects.all()


@register_model_view(CustomPrefix, "bulk_edit", path="edit", detail=False)
class CustomPrefixBulkEditView(generic.BulkEditView):
    queryset = CustomPrefix.objects.all()
    filterset = CustomPrefixFilterSet
    table = CustomPrefixTable
    form = CustomPrefixBulkEditForm


@register_model_view(CustomPrefix, "bulk_delete", path="delete", detail=False)
class CustomPrefixBulkDeleteView(generic.BulkDeleteView):
    queryset = CustomPrefix.objects.all()
    table = CustomPrefixTable


@register_model_view(CustomPrefix, "bulk_import", detail=False)
class CustomPrefixBulkImportView(generic.BulkImportView):
    queryset = CustomPrefix.objects.all()
    model_form = CustomPrefixImportForm
