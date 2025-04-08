import django_filters
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from netbox_security.models import (
    SecurityZonePolicy,
    SecurityZone,
    Address,
    AddressSet,
)

from netbox_security.choices import ActionChoices


class SecurityZonePolicyFilterSet(NetBoxModelFilterSet):
    source_zone_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        field_name="source_zone",
        to_field_name="id",
        label=_("Source Zone (ID)"),
    )
    source_zone = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        field_name="source_zone",
        to_field_name="name",
        label=_("Source Zone (Name)"),
    )
    destination_zone_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        field_name="destination_zone",
        to_field_name="id",
        label=_("Destination Zone (ID)"),
    )
    destination_zone = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        field_name="destination_zone",
        to_field_name="name",
        label=_("Destination Zone (Name)"),
    )
    source_address_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Address.objects.all(),
        field_name="source_address",
        to_field_name="id",
        label=_("Source Address (ID)"),
    )
    source_address = django_filters.ModelMultipleChoiceFilter(
        queryset=Address.objects.all(),
        field_name="source_address",
        to_field_name="name",
        label=_("Source Address (Name)"),
    )
    destination_address_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Address.objects.all(),
        field_name="destination_address",
        to_field_name="id",
        label=_("Destination Address (ID)"),
    )
    destination_address = django_filters.ModelMultipleChoiceFilter(
        queryset=Address.objects.all(),
        field_name="destination_address",
        to_field_name="name",
        label=_("Destination Address (Name)"),
    )
    address_list_id = django_filters.ModelMultipleChoiceFilter(
        method="filter_addresses",
        queryset=Address.objects.all(),
        label=_("Nat Ruleset Zones"),
    )
    actions = django_filters.MultipleChoiceFilter(
        choices=ActionChoices,
        required=False,
    )
    application = django_filters.CharFilter(
        field_name="application",
        lookup_expr="contains",
        required=False,
    )

    class Meta:
        model = SecurityZonePolicy
        fields = ["id", "name", "description", "index"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(application__contains=[value])
        )
        return queryset.filter(qs_filter)

    def filter_addresses(self, queryset, name, value):
        if not value:
            return queryset
        source_addresses = {address.source_address.pk for address in value}
        destination_addresses = {address.destination_address.pk for address in value}
        return queryset.filter(pk__in=[source_addresses, destination_addresses])
