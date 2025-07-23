import django_filters
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.filtersets import TenancyFilterSet
from utilities.filters import (
    MultiValueCharFilter,
    MultiValueNumberFilter,
)

from netbox_security.models import (
    AddressSet,
    AddressSetAssignment,
    Address,
    SecurityZone,
)
from netbox_security.mixins import (
    AssignmentFilterSet,
)


class AddressSetFilterSet(TenancyFilterSet, NetBoxModelFilterSet):
    address_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Address.objects.all(),
        field_name="addresses",
        to_field_name="id",
        label=_("Address (ID)"),
    )
    address = django_filters.ModelMultipleChoiceFilter(
        queryset=Address.objects.all(),
        field_name="addresses__name",
        to_field_name="name",
        label=_("Address (Name)"),
    )
    address_set_id = django_filters.ModelMultipleChoiceFilter(
        queryset=AddressSet.objects.all(),
        field_name="addressset_address_sets",
        to_field_name="id",
        label=_("Address Set (ID)"),
    )
    address_set = django_filters.ModelMultipleChoiceFilter(
        queryset=Address.objects.all(),
        field_name="addressset_address_sets__name",
        to_field_name="name",
        label=_("Address Set (Name)"),
    )

    class Meta:
        model = AddressSet
        fields = ["id", "name", "description", "identifier"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(identifier__icontains=value)
        )
        return queryset.filter(qs_filter)


class AddressSetAssignmentFilterSet(AssignmentFilterSet):
    address_set_id = django_filters.ModelMultipleChoiceFilter(
        queryset=AddressSet.objects.all(),
        label=_("AddressSet (ID)"),
    )
    address_set = django_filters.ModelMultipleChoiceFilter(
        field_name="address_set__name",
        queryset=AddressSet.objects.all(),
        to_field_name="name",
        label=_("Address Set (Name)"),
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
        model = AddressSetAssignment
        fields = ("id", "address_set_id", "assigned_object_type", "assigned_object_id")

    def filter_zone(self, queryset, name, value):
        if not (
            zones := SecurityZone.objects.filter(**{f"{name}__in": value})
        ).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(SecurityZone),
            assigned_object_id__in=zones.values_list("id", flat=True),
        )
