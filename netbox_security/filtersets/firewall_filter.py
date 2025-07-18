import django_filters
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.filtersets import TenancyFilterSet

from netbox_security.models import (
    FirewallFilter,
    FirewallFilterAssignment,
)
from netbox_security.mixins import (
    AssignmentFilterSet,
)
from netbox_security.choices import FamilyChoices


class FirewallFilterFilterSet(TenancyFilterSet, NetBoxModelFilterSet):
    family = django_filters.MultipleChoiceFilter(
        choices=FamilyChoices,
        required=False,
    )

    class Meta:
        model = FirewallFilter
        fields = ["id", "name", "description"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(description__icontains=value)
        return queryset.filter(qs_filter)


class FirewallFilterAssignmentFilterSet(AssignmentFilterSet):
    firewall_filter_id = django_filters.ModelMultipleChoiceFilter(
        queryset=FirewallFilter.objects.all(),
        label=_("Firewall Filter (ID)"),
    )
    firewall_filter = django_filters.ModelMultipleChoiceFilter(
        field_name="firewall_filter__name",
        queryset=FirewallFilter.objects.all(),
        to_field_name="name",
        label=_("Firewall Filter (Name)"),
    )

    class Meta:
        model = FirewallFilterAssignment
        fields = (
            "id",
            "firewall_filter_id",
            "assigned_object_type",
            "assigned_object_id",
        )
