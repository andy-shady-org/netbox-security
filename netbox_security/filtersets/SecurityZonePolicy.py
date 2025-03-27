import django_filters
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from netbox_security.models import (
    SecurityZonePolicy,
    SecurityZone,
    Address
)

from netbox_security.choices import ActionChoices


class SecurityZonePolicyFilterSet(NetBoxModelFilterSet):
    source_zone_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        field_name="source_zone__id",
        to_field_name='id',
        label=_('Source Zone (ID)'),
    )
    source_zone = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        field_name="source_zone__name",
        to_field_name='name',
        label=_('Source Zone (Name)'),
    )
    destination_zone_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        field_name="destination_zone__id",
        to_field_name='id',
        label=_('Destination Zone (ID)'),
    )
    destination_zone = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        field_name="destination_zone__name",
        to_field_name='name',
        label=_('Destination Zone (Name)'),
    )
    source_address_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Address.objects.all(),
        field_name="source_address__id",
        to_field_name='id',
        label=_('Source Address List (ID)'),
    )
    source_address = django_filters.ModelMultipleChoiceFilter(
        queryset=Address.objects.all(),
        field_name="source_address__name",
        to_field_name='name',
        label=_('Source Address List (Name)'),
    )
    destination_address_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Address.objects.all(),
        field_name="destination_address__id",
        to_field_name='id',
        label=_('Destination Address List (ID)'),
    )
    destination_address = django_filters.ModelMultipleChoiceFilter(
        queryset=Address.objects.all(),
        field_name="destination_address__name",
        to_field_name='name',
        label=_('Destination Address List (Name)'),
    )
    actions = django_filters.MultipleChoiceFilter(
        choices=ActionChoices,
        required=False,
    )

    class Meta:
        model = SecurityZonePolicy
        fields = ['id', 'name', 'description']

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
