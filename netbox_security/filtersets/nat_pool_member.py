import django_filters
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from ipam.models import IPAddress, Prefix, IPRange
from ipam.choices import IPAddressStatusChoices

from netbox_security.models import (
    NatPool,
    NatPoolMember,
)
from netbox_security.mixins import PortsFilterSet


class NatPoolMemberFilterSet(PortsFilterSet, NetBoxModelFilterSet):
    pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=NatPool.objects.all(),
        field_name="pool",
        to_field_name="id",
        label=_("NAT Pool (ID)"),
    )
    pool = django_filters.ModelMultipleChoiceFilter(
        queryset=NatPool.objects.all(),
        field_name="pool__name",
        to_field_name="name",
        label=_("NAT Pool (Name)"),
    )
    address_id = django_filters.ModelMultipleChoiceFilter(
        field_name="address",
        queryset=IPAddress.objects.all(),
        to_field_name="id",
        label=_("Address (ID)"),
    )
    address = django_filters.ModelMultipleChoiceFilter(
        field_name="address__address",
        queryset=IPAddress.objects.all(),
        to_field_name="address",
        label=_("Address"),
    )
    prefix_id = django_filters.ModelMultipleChoiceFilter(
        field_name="prefix",
        queryset=Prefix.objects.all(),
        to_field_name="id",
        label=_("Prefix (ID)"),
    )
    prefix = django_filters.ModelMultipleChoiceFilter(
        field_name="prefix__prefix",
        queryset=Prefix.objects.all(),
        to_field_name="prefix",
        label=_("Prefix (Prefix)"),
    )
    address_range_id = django_filters.ModelMultipleChoiceFilter(
        field_name="address_range",
        queryset=IPRange.objects.all(),
        to_field_name="id",
        label=_("IPRange (ID)"),
    )
    address_range = django_filters.ModelMultipleChoiceFilter(
        field_name="address_range__start_address",
        queryset=IPRange.objects.all(),
        to_field_name="start_address",
        label=_("IPRange (Start Address)"),
    )
    status = django_filters.MultipleChoiceFilter(
        choices=IPAddressStatusChoices,
        required=False,
    )

    class Meta:
        model = NatPoolMember
        fields = ["id", "name"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter)
