from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from tenancy.views import ObjectContactsView
from utilities.views import register_model_view, ViewTab

from netbox_security.models import NatPool, NatPoolMember, NatPoolAssignment

from netbox_security.forms import (
    NatPoolForm,
    NatPoolFilterForm,
    NatPoolBulkEditForm,
    NatPoolImportForm,
    NatPoolAssignmentForm,
)
from netbox_security.filtersets import NatPoolFilterSet, NatPoolMemberFilterSet
from netbox_security.tables import NatPoolTable, NatPoolMemberTable


__all__ = (
    "NatPoolView",
    "NatPoolListView",
    "NatPoolEditView",
    "NatPoolDeleteView",
    "NatPoolBulkEditView",
    "NatPoolBulkDeleteView",
    "NatPoolBulkImportView",
    "NatPoolNatPoolMembersView",
    "NatPoolContactsView",
    "NatPoolAssignmentEditView",
    "NatPoolAssignmentDeleteView",
)


@register_model_view(NatPool)
class NatPoolView(generic.ObjectView):
    queryset = NatPool.objects.annotate(member_count=Count("natpoolmember_pools"))
    template_name = "netbox_security/natpool.html"

    def get_extra_context(self, request, instance):
        sess = NatPoolMember.objects.filter(Q(pool=instance))
        sess = sess.distinct()
        sess_table = NatPoolMemberTable(sess)
        return {"related_session_table": sess_table}


@register_model_view(NatPool, "list", path="", detail=False)
class NatPoolListView(generic.ObjectListView):
    queryset = NatPool.objects.all()
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
    default_return_url = "plugins:netbox_security:natpool_list"


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
    default_return_url = "plugins:netbox_security:natpool_list"


@register_model_view(NatPool, name="members")
class NatPoolNatPoolMembersView(generic.ObjectChildrenView):
    template_name = "netbox_security/natpool_members.html"
    queryset = NatPool.objects.all()
    child_model = NatPoolMember
    table = NatPoolMemberTable
    filterset = NatPoolMemberFilterSet
    actions = []
    tab = ViewTab(
        label=_("NAT Pool Members"),
        badge=lambda obj: NatPoolMember.objects.filter(pool=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(pool=parent)


@register_model_view(NatPool, "contacts")
class NatPoolContactsView(ObjectContactsView):
    queryset = NatPool.objects.all()


@register_model_view(NatPoolAssignment, "add", detail=False)
@register_model_view(NatPoolAssignment, "edit")
class NatPoolAssignmentEditView(generic.ObjectEditView):
    queryset = NatPoolAssignment.objects.all()
    form = NatPoolAssignmentForm

    def alter_object(self, instance, request, args, kwargs):
        if not instance.pk:
            content_type = get_object_or_404(
                ContentType, pk=request.GET.get("assigned_object_type")
            )
            instance.assigned_object = get_object_or_404(
                content_type.model_class(), pk=request.GET.get("assigned_object_id")
            )
        return instance

    def get_extra_addanother_params(self, request):
        return {
            "assigned_object_type": request.GET.get("assigned_object_type"),
            "assigned_object_id": request.GET.get("assigned_object_id"),
        }


@register_model_view(NatPoolAssignment, "delete")
class NatPoolAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = NatPoolAssignment.objects.all()
