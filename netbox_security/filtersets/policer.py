import django_filters
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.filtersets import TenancyFilterSet

from netbox_security.models import (
    Policer,
    PolicerAssignment,
)
from netbox_security.mixins import (
    AssignmentFilterSet,
)
from netbox_security.choices import (
    LossPriorityChoices,
    ForwardingClassChoices,
)


class PolicerFilterSet(TenancyFilterSet, NetBoxModelFilterSet):
    loss_priority = django_filters.MultipleChoiceFilter(
        choices=LossPriorityChoices,
        required=False,
    )
    forwarding_class = django_filters.MultipleChoiceFilter(
        choices=ForwardingClassChoices,
        required=False,
    )
    logical_interface_policer = django_filters.BooleanFilter()
    physical_interface_policer = django_filters.BooleanFilter()
    discard = django_filters.BooleanFilter()
    out_of_profile = django_filters.BooleanFilter()

    class Meta:
        model = Policer
        fields = [
            "id",
            "name",
            "description",
            "bandwidth_limit",
            "bandwidth_percent",
            "burst_size_limit",
        ]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(bandwidth_limit=value)
            | Q(bandwidth_percent=value)
            | Q(burst_size_limit=value)
        )
        return queryset.filter(qs_filter)


class PolicerAssignmentFilterSet(AssignmentFilterSet):
    policer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Policer.objects.all(),
        label=_("Policer (ID)"),
    )
    policer = django_filters.ModelMultipleChoiceFilter(
        field_name="policer__name",
        queryset=Policer.objects.all(),
        to_field_name="name",
        label=_("Policer (Name)"),
    )

    class Meta:
        model = PolicerAssignment
        fields = ("id", "policer_id", "assigned_object_type", "assigned_object_id")
