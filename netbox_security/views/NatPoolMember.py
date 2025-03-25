from netbox.views import generic

from netbox_security.models import NatPoolMember
from netbox_security.tables import NatPoolMemberTable
from netbox_security.filtersets import NatPoolMemberFilterSet
from netbox_security.forms import (
    NatPoolMemberFilterForm,
    NatPoolMemberForm,
    NatPoolMemberBulkEditForm,
    NatPoolMemberImportForm
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


class NatPoolMemberView(generic.ObjectView):
    queryset = NatPoolMember.objects.all()
    template_name = 'netbox_security/natpoolmember.html'


class NatPoolMemberListView(generic.ObjectListView):
    queryset = NatPoolMember.objects.all()
    filterset = NatPoolMemberFilterSet
    filterset_form = NatPoolMemberFilterForm
    table = NatPoolMemberTable


class NatPoolMemberEditView(generic.ObjectEditView):
    queryset = NatPoolMember.objects.all()
    form = NatPoolMemberForm


class NatPoolMemberDeleteView(generic.ObjectDeleteView):
    queryset = NatPoolMember.objects.all()
    default_return_url = 'plugins:netbox_security:natpoolmember_list'


class NatPoolMemberBulkEditView(generic.BulkEditView):
    queryset = NatPoolMember.objects.all()
    filterset = NatPoolMemberFilterSet
    table = NatPoolMemberTable
    form = NatPoolMemberBulkEditForm


class NatPoolMemberBulkImportView(generic.BulkImportView):
    queryset = NatPoolMember.objects.all()
    model_form = NatPoolMemberImportForm


class NatPoolMemberBulkDeleteView(generic.BulkDeleteView):
    queryset = NatPoolMember.objects.all()
    table = NatPoolMemberTable
    default_return_url = 'plugins:netbox_security:natpoolmember_list'
