from netbox.views import generic
from utilities.views import register_model_view
from netbox_security.models import NatPoolMember
from netbox_security.tables import NatPoolMemberTable
from netbox_security.filtersets import NatPoolMemberFilterSet
from netbox_security.forms import (
    NatPoolMemberFilterForm,
    NatPoolMemberForm,
    NatPoolMemberBulkEditForm,
    NatPoolMemberImportForm,
)


__all__ = (
    "NatPoolMemberView",
    "NatPoolMemberListView",
    "NatPoolMemberEditView",
    "NatPoolMemberDeleteView",
    "NatPoolMemberBulkEditView",
    "NatPoolMemberBulkImportView",
    "NatPoolMemberBulkDeleteView",
)


@register_model_view(NatPoolMember)
class NatPoolMemberView(generic.ObjectView):
    queryset = NatPoolMember.objects.all()
    template_name = "netbox_security/natpoolmember.html"


@register_model_view(NatPoolMember, "list", path="", detail=False)
class NatPoolMemberListView(generic.ObjectListView):
    queryset = NatPoolMember.objects.all()
    filterset = NatPoolMemberFilterSet
    filterset_form = NatPoolMemberFilterForm
    table = NatPoolMemberTable


@register_model_view(NatPoolMember, "add", detail=False)
@register_model_view(NatPoolMember, "edit")
class NatPoolMemberEditView(generic.ObjectEditView):
    queryset = NatPoolMember.objects.all()
    form = NatPoolMemberForm


@register_model_view(NatPoolMember, "delete")
class NatPoolMemberDeleteView(generic.ObjectDeleteView):
    queryset = NatPoolMember.objects.all()


@register_model_view(NatPoolMember, "bulk_edit", path="edit", detail=False)
class NatPoolMemberBulkEditView(generic.BulkEditView):
    queryset = NatPoolMember.objects.all()
    filterset = NatPoolMemberFilterSet
    table = NatPoolMemberTable
    form = NatPoolMemberBulkEditForm


@register_model_view(NatPoolMember, "bulk_import", detail=False)
class NatPoolMemberBulkImportView(generic.BulkImportView):
    queryset = NatPoolMember.objects.all()
    model_form = NatPoolMemberImportForm


@register_model_view(NatPoolMember, "bulk_delete", path="delete", detail=False)
class NatPoolMemberBulkDeleteView(generic.BulkDeleteView):
    queryset = NatPoolMember.objects.all()
    table = NatPoolMemberTable
