import django_filters
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filters import (
    ContentTypeFilter,
    MultiValueCharFilter,
    MultiValueNumberFilter,
)

from netbox_security.models import (
    AddressList,
    Address,
    AddressSet,
    AddressListAssignment,
    SecurityZone,
    SecurityZonePolicy,
)
from netbox_security.mixins import (
    AssignmentFilterSet,
)


class AddressListFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()
    address = MultiValueCharFilter(
        method="filter_address",
        field_name="name",
        label=_("Address (name)"),
    )
    address_id = MultiValueNumberFilter(
        method="filter_address",
        field_name="pk",
        label=_("Address (ID)"),
    )
    addressset = MultiValueCharFilter(
        method="filter_addressset",
        field_name="name",
        label=_("Address Set (name)"),
    )
    addressset_id = MultiValueNumberFilter(
        method="filter_addressset",
        field_name="pk",
        label=_("Address Set (ID)"),
    )
    source_address_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZonePolicy.objects.all(),
        field_name="securityzonepolicy_source_address",
        to_field_name="id",
        label=_("Source Address List (ID)"),
    )
    destination_address_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZonePolicy.objects.all(),
        field_name="securityzonepolicy_destination_address",
        to_field_name="id",
        label=_("Destination Address List (ID)"),
    )

    class Meta:
        model = AddressList
        fields = ["id", "assigned_object_type", "assigned_object_id"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter)

    def filter_address(self, queryset, name, value):
        if not (addresses := Address.objects.filter(**{f"{name}__in": value})).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(Address),
            assigned_object_id__in=addresses.values_list("id", flat=True),
        )

    def filter_addressset(self, queryset, name, value):
        if not (
            addresses := AddressSet.objects.filter(**{f"{name}__in": value})
        ).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(AddressSet),
            assigned_object_id__in=addresses.values_list("id", flat=True),
        )


class AddressListAssignmentFilterSet(AssignmentFilterSet):
    address_list_id = django_filters.ModelMultipleChoiceFilter(
        queryset=AddressList.objects.all(),
        label=_("Address List (ID)"),
    )
    address_list = django_filters.ModelMultipleChoiceFilter(
        field_name="address_list__name",
        queryset=AddressList.objects.all(),
        to_field_name="name",
        label=_("Address List (Name)"),
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
        model = AddressListAssignment
        fields = ("id", "address_list_id", "assigned_object_type", "assigned_object_id")

    def filter_zone(self, queryset, name, value):
        if not (
            zones := SecurityZone.objects.filter(**{f"{name}__in": value})
        ).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(SecurityZone),
            assigned_object_id__in=zones.values_list("id", flat=True),
        )
