import django_filters
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.filtersets import TenancyFilterSet
from utilities.filters import (
    ContentTypeFilter,
    MultiValueCharFilter,
    MultiValueNumberFilter,
)
from dcim.models import Device, VirtualDeviceContext

from netbox_security.models import (
    Policer,
    PolicerAssignment,
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


class PolicerAssignmentFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()
    policer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=PolicerAssignment.objects.all(),
        label=_("Policer (ID)"),
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
        method="filter_context",
        field_name="name",
        label=_("Virtual Device Context (name)"),
    )
    virtualdevicecontext_id = MultiValueNumberFilter(
        method="filter_context",
        field_name="pk",
        label=_("Virtual Device Context (ID)"),
    )

    class Meta:
        model = PolicerAssignment
        fields = ("id", "policer_id", "assigned_object_type", "assigned_object_id")

    def filter_device(self, queryset, name, value):
        if not (devices := Device.objects.filter(**{f"{name}__in": value})).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(Device),
            assigned_object_id__in=devices.values_list("id", flat=True),
        )

    def filter_context(self, queryset, name, value):
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
