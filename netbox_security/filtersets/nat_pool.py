import django_filters
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filters import (
    MultiValueCharFilter,
    MultiValueNumberFilter,
)
from ipam.choices import IPAddressStatusChoices
from virtualization.models import VirtualMachine

from netbox_security.models import (
    NatPool,
    NatPoolAssignment,
)
from netbox_security.mixins import (
    AssignmentFilterSet,
)
from netbox_security.choices import PoolTypeChoices


class NatPoolFilterSet(NetBoxModelFilterSet):
    pool_type = django_filters.MultipleChoiceFilter(
        choices=PoolTypeChoices,
        required=False,
    )
    status = django_filters.MultipleChoiceFilter(
        choices=IPAddressStatusChoices,
        required=False,
    )

    class Meta:
        model = NatPool
        fields = ["id", "name", "description"]


def search(self, queryset, name, value):
    """Perform the filtered search."""
    if not value.strip():
        return queryset
    qs_filter = Q(name__icontains=value) | Q(description__icontains=value)
    return queryset.filter(qs_filter)


class NatPoolAssignmentFilterSet(AssignmentFilterSet):
    pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=NatPool.objects.all(),
        label=_("NAT Pool (ID)"),
    )
    pool = django_filters.ModelMultipleChoiceFilter(
        field_name="pool__name",
        queryset=NatPool.objects.all(),
        to_field_name="name",
        label=_("NAT Pool (Name)"),
    )
    virtualmachine = MultiValueCharFilter(
        method="filter_virtual_machine",
        field_name="name",
        label=_("Virtual Machine (name)"),
    )
    virtualmachine_id = MultiValueNumberFilter(
        method="filter_virtual_machine",
        field_name="pk",
        label=_("Virtual Machine (ID)"),
    )

    class Meta:
        model = NatPoolAssignment
        fields = ("id", "pool_id", "assigned_object_type", "assigned_object_id")

    def filter_virtual_machine(self, queryset, name, value):
        if not (
            devices := VirtualMachine.objects.filter(**{f"{name}__in": value})
        ).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(VirtualMachine),
            assigned_object_id__in=devices.values_list("id", flat=True),
        )
