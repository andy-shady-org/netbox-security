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
from dcim.models import Device, VirtualDeviceContext
from ipam.choices import IPAddressStatusChoices

from netbox_security.models import (
    NatPool,
    NatPoolAssignment,
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


class NatPoolAssignmentFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()
    pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=NatPool.objects.all(),
        label=_("NAT Pool (ID)"),
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
        model = NatPoolAssignment
        fields = ("id", "pool_id", "assigned_object_type", "assigned_object_id")

    def filter_device(self, queryset, name, value):
        devices = Device.objects.filter(**{f"{name}__in": value})
        if not devices.exists():
            return queryset.none()
        device_ids = []
        device_ids.extend(
            Device.objects.filter(**{f"{name}__in": value}).values_list("id", flat=True)
        )
        return queryset.filter(
            Q(
                assigned_object_type=ContentType.objects.get_for_model(Device),
                assigned_object_id__in=device_ids,
            )
        )

    def filter_context(self, queryset, name, value):
        devices = VirtualDeviceContext.objects.filter(**{f"{name}__in": value})
        if not devices.exists():
            return queryset.none()
        device_ids = []
        device_ids.extend(
            VirtualDeviceContext.objects.filter(**{f"{name}__in": value}).values_list(
                "id", flat=True
            )
        )
        return queryset.filter(
            Q(
                assigned_object_type=ContentType.objects.get_for_model(Device),
                assigned_object_id__in=device_ids,
            )
        )
