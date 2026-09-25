from django.utils.translation import gettext_lazy as _
from django.db.models import Count

from netbox.context import current_request
from netbox.views import generic
from utilities.views import register_model_view, ViewTab
from netbox.object_actions import BulkExport

from dcim.models import Device, VirtualDeviceContext
from virtualization.models import VirtualMachine

from dcim.tables import DeviceTable, VirtualDeviceContextTable
from virtualization.tables import VirtualMachineTable

from netbox_security.utils.assignment import get_assigned_object
from netbox_security.constants import POOL_ASSIGNMENT_MODELS
from netbox_security.models import NatPool, NatPoolMember, NatPoolAssignment

from netbox_security.forms import (
    NatPoolForm,
    NatPoolFilterForm,
    NatPoolBulkEditForm,
    NatPoolImportForm,
    NatPoolAssignmentForm,
    NatPoolAssignmentFilterForm,
)
from netbox_security.filtersets import (
    NatPoolFilterSet,
    NatPoolMemberFilterSet,
    NatPoolAssignmentFilterSet,
)
from netbox_security.tables import (
    NatPoolTable,
    NatPoolMemberTable,
    NatPoolAssignmentTable,
)

__all__ = (
    "NatPoolView",
    "NatPoolListView",
    "NatPoolEditView",
    "NatPoolDeleteView",
    "NatPoolBulkEditView",
    "NatPoolBulkDeleteView",
    "NatPoolBulkImportView",
    "NatPoolNatPoolMembersView",
    "NatPoolAssignmentEditView",
    "NatPoolAssignmentDeleteView",
    "NatPoolAssignmentListView",
    "NatPoolAssignmentBulkDeleteView",
)


def _natpoolmember_count(obj):
    request = current_request.get()
    if request is None or getattr(request, "user", None) is None:
        return 0
    return obj.natpoolmember_pools.restrict(request.user, "view").count()


@register_model_view(NatPool)
class NatPoolView(generic.ObjectView):
    queryset = NatPool.objects.annotate(member_count=Count("natpoolmember_pools"))
    template_name = "netbox_security/natpool.html"

    def get_extra_context(self, request, instance):
        table_definitions = {
            "device_assignments_table": (
                DeviceTable,
                Device.objects.restrict(request.user, "view").filter(
                    nat_pools__pool=instance
                ),
            ),
            "virtual_device_assignments_table": (
                VirtualDeviceContextTable,
                VirtualDeviceContext.objects.restrict(request.user, "view").filter(
                    nat_pools__pool=instance
                ),
            ),
            "virtual_machine_assignments_table": (
                VirtualMachineTable,
                VirtualMachine.objects.restrict(request.user, "view").filter(
                    nat_pools__pool=instance
                ),
            ),
        }
        context = {}
        for name, (table_class, queryset) in table_definitions.items():
            table = table_class(queryset, orderable=False)
            table.configure(request)
            context[name] = table

        return context


@register_model_view(NatPool, "list", path="", detail=False)
class NatPoolListView(generic.ObjectListView):
    queryset = NatPool.objects.annotate(member_count=Count("natpoolmember_pools"))
    filterset = NatPoolFilterSet
    filterset_form = NatPoolFilterForm
    table = NatPoolTable


@register_model_view(NatPool, "add", detail=False)
@register_model_view(NatPool, "edit")
class NatPoolEditView(generic.ObjectEditView):
    queryset = NatPool.objects.all()
    form = NatPoolForm


@register_model_view(NatPool, "delete")
class NatPoolDeleteView(generic.ObjectDeleteView):
    queryset = NatPool.objects.all()


@register_model_view(NatPool, "bulk_edit", path="edit", detail=False)
class NatPoolBulkEditView(generic.BulkEditView):
    queryset = NatPool.objects.all()
    filterset = NatPoolFilterSet
    table = NatPoolTable
    form = NatPoolBulkEditForm


@register_model_view(NatPool, "bulk_import", detail=False)
class NatPoolBulkImportView(generic.BulkImportView):
    queryset = NatPool.objects.all()
    model_form = NatPoolImportForm


@register_model_view(NatPool, "bulk_delete", path="delete", detail=False)
class NatPoolBulkDeleteView(generic.BulkDeleteView):
    queryset = NatPool.objects.all()
    table = NatPoolTable


@register_model_view(NatPool, name="members")
class NatPoolNatPoolMembersView(generic.ObjectChildrenView):
    template_name = "netbox_security/natpool_members.html"
    queryset = NatPool.objects.all().prefetch_related("natpoolmember_pools")
    child_model = NatPoolMember
    table = NatPoolMemberTable
    filterset = NatPoolMemberFilterSet
    tab = ViewTab(
        label=_("NAT Pool Members"),
        permission="netbox_security.view_natpoolmember",
        badge=lambda obj: _natpoolmember_count(obj),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.natpoolmember_pools.restrict(request.user, "view")


@register_model_view(NatPoolAssignment, "list", path="", detail=False)
class NatPoolAssignmentListView(generic.ObjectListView):
    queryset = NatPoolAssignment.objects.all()
    filterset = NatPoolAssignmentFilterSet
    filterset_form = NatPoolAssignmentFilterForm
    table = NatPoolAssignmentTable
    actions = [BulkExport]


@register_model_view(NatPoolAssignment, "add", detail=False)
@register_model_view(NatPoolAssignment, "edit")
class NatPoolAssignmentEditView(generic.ObjectEditView):
    queryset = NatPoolAssignment.objects.all()
    form = NatPoolAssignmentForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if not obj.pk:
            obj.assigned_object = get_assigned_object(
                request,
                allowed_content_type_filter=POOL_ASSIGNMENT_MODELS,
            )

        return obj

    def get_extra_addanother_params(self, request):
        return {
            "assigned_object_type": request.GET.get("assigned_object_type"),
            "assigned_object_id": request.GET.get("assigned_object_id"),
        }


@register_model_view(NatPoolAssignment, "delete")
class NatPoolAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = NatPoolAssignment.objects.all()


@register_model_view(NatPoolAssignment, "bulk_delete", path="delete", detail=False)
class NatPoolAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = NatPoolAssignment.objects.all()
    table = NatPoolAssignmentTable
