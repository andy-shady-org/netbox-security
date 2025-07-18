import django_filters
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from netaddr.core import AddrFormatError
from netaddr import IPNetwork
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.filtersets import TenancyFilterSet
from utilities.filters import (
    MultiValueCharFilter,
    MultiValueNumberFilter,
)

from ipam.models import IPRange

from netbox_security.models import (
    Address,
    AddressSet,
    AddressAssignment,
    SecurityZone,
)
from netbox_security.mixins import (
    AssignmentFilterSet,
)


class AddressFilterSet(TenancyFilterSet, NetBoxModelFilterSet):
    address = django_filters.CharFilter(
        method="filter_address",
        label=_("Value"),
    )
    address_set_id = django_filters.ModelMultipleChoiceFilter(
        queryset=AddressSet.objects.all(),
        field_name="addressset_addresses",
        to_field_name="id",
        label=_("Address Set (ID)"),
    )
    ip_range_id = django_filters.ModelMultipleChoiceFilter(
        field_name="ip_range",
        queryset=IPRange.objects.all(),
        to_field_name="id",
        label=_("IPRange (ID)"),
    )
    ip_range = django_filters.ModelMultipleChoiceFilter(
        field_name="ip_range__start_address",
        queryset=IPRange.objects.all(),
        to_field_name="start_address",
        label=_("IPRange (Start Address)"),
    )

    class Meta:
        model = Address
        fields = ["id", "name", "description", "dns_name", "identifier"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(identifier__icontains=value)
            | Q(dns_name=value)
        )
        return queryset.filter(qs_filter)

    def filter_address(self, queryset, name, value):
        if not value.strip():
            return queryset
        try:
            query = str(IPNetwork(value).cidr)
            return queryset.filter(address=query)
        except (AddrFormatError, ValueError):
            return queryset.none()


class AddressAssignmentFilterSet(AssignmentFilterSet):
    address_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Address.objects.all(),
        label=_("Address (ID)"),
    )
    address = django_filters.ModelMultipleChoiceFilter(
        field_name="address__name",
        queryset=Address.objects.all(),
        to_field_name="name",
        label=_("Address (Name)"),
    )
    security_zone = MultiValueCharFilter(
        method="filter_zone",
        field_name="name",
        label=_("Security Zone (name)"),
    )
    security_zone_id = MultiValueNumberFilter(
        method="filter_zone",
        field_name="pk",
        label=_("Security Zone (ID)"),
    )

    class Meta:
        model = AddressAssignment
        fields = ("id", "address_id", "assigned_object_type", "assigned_object_id")

    def filter_zone(self, queryset, name, value):
        if not (
            zones := SecurityZone.objects.filter(**{f"{name}__in": value})
        ).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(SecurityZone),
            assigned_object_id__in=zones.values_list("id", flat=True),
        )
