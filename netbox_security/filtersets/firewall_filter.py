import django_filters
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from netbox.filtersets import PrimaryModelFilterSet
from tenancy.filtersets import TenancyFilterSet
from utilities.filtersets import register_filterset
from utilities.filters import (
    MultiValueCharFilter,
    MultiValueNumberFilter,
)

from dcim.models import Device, VirtualDeviceContext

from netbox_security.models import (
    FirewallFilter,
    FirewallFilterAssignment,
)
from netbox_security.mixins import (
    AssignmentFilterSet,
)
from netbox_security.choices import FamilyChoices

__all__ = (
    "FirewallFilterFilterSet",
    "FirewallFilterAssignmentFilterSet",
)


@register_filterset
class FirewallFilterFilterSet(TenancyFilterSet, PrimaryModelFilterSet):
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


@register_filterset
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
    device = MultiValueCharFilter(
        method="filter_device",
        field_name="name",
        label=_("Device (name)"),
    )
    device_id = MultiValueNumberFilter(
        method="filter_device",
        field_name="pk",
        label=_("Device (ID)"),
    )
    virtualdevicecontext = MultiValueCharFilter(
        method="filter_virtualdevicecontext",
        field_name="name",
        label=_("Virtual Device Context (name)"),
    )
    virtualdevicecontext_id = MultiValueNumberFilter(
        method="filter_virtualdevicecontext",
        field_name="pk",
        label=_("Virtual Device Context (ID)"),
    )

    class Meta:
        model = FirewallFilterAssignment
        fields = (
            "id",
            "firewall_filter_id",
            "assigned_object_type",
            "assigned_object_id",
        )

    def filter_device(self, queryset, name, value):
        if not (devices := Device.objects.filter(**{f"{name}__in": value})).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(Device),
            assigned_object_id__in=devices.values_list("id", flat=True),
        )

    def filter_virtualdevicecontext(self, queryset, name, value):
        if not (
            devices := VirtualDeviceContext.objects.filter(**{f"{name}__in": value})
        ).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(
                VirtualDeviceContext
            ),
            assigned_object_id__in=devices.values_list("id", flat=True),
        )
