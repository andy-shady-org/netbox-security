from django.utils.translation import gettext_lazy as _
from django.db.models import Count, F, IntegerField, OuterRef, Q, Subquery, Value
from django.db.models.functions import Coalesce

from ipam.models import IPAddress, IPRange, Prefix
from dcim.models import Device, VirtualDeviceContext
from virtualization.models import VirtualMachine
from netbox_security.models import (
    Address,
    NatPoolMember,
    NatRule,
    SecurityZone,
)
from netbox_security.utils import get_address_set_hierarchy
from netbox_security.utils.policy_candidates import add_policy_candidates

from netbox.context import current_request
from netbox.views import generic
from utilities.views import register_model_view, ViewTab


def _count_subquery(qs):
    return Coalesce(
        Subquery(
            qs.order_by()
            .annotate(_group=Value(1))
            .values("_group")
            .annotate(c=Count("pk", distinct=True))
            .values("c")[:1]
        ),
        Value(0),
        output_field=IntegerField(),
    )


def _annotate_ipam_security_queryset(
    queryset,
    *,
    user,
    assigned_object_model,
    nat_pool_member_field,
    nat_rule_source_field,
    nat_rule_destination_field,
):
    nat_pool_member_filter = {f"{nat_pool_member_field}_id": OuterRef("pk")}
    nat_rule_source_filter = {nat_rule_source_field: OuterRef("pk")}
    nat_rule_destination_filter = {nat_rule_destination_field: OuterRef("pk")}

    return queryset.annotate(
        nat_pool_member_count=_count_subquery(
            NatPoolMember.objects.restrict(user, "view").filter(
                **nat_pool_member_filter
            )
        ),
        nat_rule_count=_count_subquery(
            NatRule.objects.restrict(user, "view").filter(
                Q(**nat_rule_source_filter) | Q(**nat_rule_destination_filter)
            )
        ),
        address_count=_count_subquery(
            Address.objects.restrict(user, "view").filter(
                assigned_object_type__app_label="ipam",
                assigned_object_type__model=assigned_object_model,
                assigned_object_id=OuterRef("pk"),
            )
        ),
        security_zone_count=_count_subquery(
            SecurityZone.objects.restrict(user, "view")
            .filter(
                addresses__address__assigned_object_type__app_label="ipam",
                addresses__address__assigned_object_type__model=assigned_object_model,
                addresses__address__assigned_object_id=OuterRef("pk"),
            )
            .distinct()
        ),
    ).annotate(
        related_total_count=(
            F("nat_pool_member_count")
            + F("nat_rule_count")
            + F("address_count")
            + F("security_zone_count")
        )
    )


def _annotate_ipaddress_queryset(queryset, *, user):
    return _annotate_ipam_security_queryset(
        queryset,
        user=user,
        assigned_object_model="ipaddress",
        nat_pool_member_field="address",
        nat_rule_source_field="source_addresses",
        nat_rule_destination_field="destination_addresses",
    )


def _annotate_prefix_queryset(queryset, *, user):
    return _annotate_ipam_security_queryset(
        queryset,
        user=user,
        assigned_object_model="prefix",
        nat_pool_member_field="prefix",
        nat_rule_source_field="source_prefixes",
        nat_rule_destination_field="destination_prefixes",
    )


def _annotate_iprange_queryset(queryset, *, user):
    return _annotate_ipam_security_queryset(
        queryset,
        user=user,
        assigned_object_model="iprange",
        nat_pool_member_field="address_range",
        nat_rule_source_field="source_ranges",
        nat_rule_destination_field="destination_ranges",
    )


def _related_total_count(obj, model, annotate_queryset):
    # Badge callbacks receive only the object; resolve the user from this request.
    request = current_request.get()
    if request is None or getattr(request, "user", None) is None:
        return 0

    # Recompute for this user instead of trusting annotations from another queryset.
    return (
        annotate_queryset(
            model.objects.restrict(request.user, "view").filter(pk=obj.pk),
            user=request.user,
        )
        .values_list("related_total_count", flat=True)
        .first()
        or 0
    )


def _ipaddress_related_total_count(obj):
    return _related_total_count(obj, IPAddress, _annotate_ipaddress_queryset)


def _prefix_related_total_count(obj):
    return _related_total_count(obj, Prefix, _annotate_prefix_queryset)


def _iprange_related_total_count(obj):
    return _related_total_count(obj, IPRange, _annotate_iprange_queryset)


def _policy_context(app_label, model, object_id, *, user, include_candidates=False):
    return get_address_set_hierarchy(
        user=user,
        app_label=app_label,
        model=model,
        object_id=object_id,
        include_candidates=include_candidates,
    )


@register_model_view(Device, name="security")
class DeviceSecurityView(generic.ObjectView):
    queryset = Device.objects.all()
    template_name = "netbox_security/device/security.html"
    tab = ViewTab(
        label=_("Security"),
        hide_if_empty=True,
    )


@register_model_view(VirtualDeviceContext, name="security")
class VirtualDeviceContextSecurityView(generic.ObjectView):
    queryset = VirtualDeviceContext.objects.all()
    template_name = "netbox_security/virtual_device_context/security.html"
    tab = ViewTab(
        label=_("Security"),
        hide_if_empty=True,
    )


@register_model_view(VirtualMachine, name="security")
class VirtualMachineSecurityView(generic.ObjectView):
    queryset = VirtualMachine.objects.all()
    template_name = "netbox_security/virtualmachine/security.html"
    tab = ViewTab(
        label=_("Security"),
        hide_if_empty=True,
    )


@register_model_view(IPAddress, name="security")
class IPAddressSecurityView(generic.ObjectView):
    queryset = IPAddress.objects.all()
    template_name = "netbox_security/ipaddress/security.html"
    tab = ViewTab(
        label=_("Security"),
        badge=_ipaddress_related_total_count,
        hide_if_empty=True,
    )

    def get_extra_context(self, request, instance):
        context = _policy_context(
            "ipam",
            "ipaddress",
            instance.pk,
            user=request.user,
            include_candidates=True,
        )
        return {
            "policy_context": add_policy_candidates(
                context, instance, user=request.user
            )
        }


@register_model_view(Prefix, name="security")
class PrefixSecurityView(generic.ObjectView):
    queryset = Prefix.objects.all()
    template_name = "netbox_security/prefix/security.html"
    tab = ViewTab(
        label=_("Security"),
        badge=_prefix_related_total_count,
        hide_if_empty=True,
    )

    def get_extra_context(self, request, instance):
        return {
            "policy_context": _policy_context(
                "ipam",
                "prefix",
                instance.pk,
                user=request.user,
            ),
        }


@register_model_view(IPRange, name="security")
class IPRangeSecurityView(generic.ObjectView):
    queryset = IPRange.objects.all()
    template_name = "netbox_security/iprange/security.html"
    tab = ViewTab(
        label=_("Security"),
        badge=_iprange_related_total_count,
        hide_if_empty=True,
    )

    def get_extra_context(self, request, instance):
        return {
            "policy_context": _policy_context(
                "ipam",
                "iprange",
                instance.pk,
                user=request.user,
            ),
        }
