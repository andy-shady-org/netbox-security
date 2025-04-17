import django_filters
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from netaddr.core import AddrFormatError
from netaddr import IPNetwork
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.filtersets import TenancyFilterSet
from utilities.filters import (
    ContentTypeFilter,
    MultiValueCharFilter,
    MultiValueNumberFilter,
)

from dcim.models import Device, VirtualDeviceContext

from netbox_security.models import (
    Address,
    AddressSet,
    AddressAssignment,
    SecurityZone,
)


class AddressFilterSet(TenancyFilterSet, NetBoxModelFilterSet):
    value = django_filters.CharFilter(
        method="filter_value",
        label=_("Value"),
    )
    address_set_id = django_filters.ModelMultipleChoiceFilter(
        queryset=AddressSet.objects.all(),
        field_name="addressset_addresses",
        to_field_name="id",
        label=_("Address Set (ID)"),
    )

    class Meta:
        model = Address
        fields = ["id", "name", "description"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(description__icontains=value)
        return queryset.filter(qs_filter)

    def filter_value(self, queryset, name, value):
        if not value.strip():
            return queryset
        try:
            query = str(IPNetwork(value).cidr)
            return queryset.filter(value=query)
        except (AddrFormatError, ValueError):
            return queryset.none()


class AddressAssignmentFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()
    address_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Address.objects.all(),
        label=_("Address (ID)"),
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
    securityzone = MultiValueCharFilter(
        method="filter_zone",
        field_name="name",
        label=_("Security Zone (name)"),
    )
    securityzone_id = MultiValueNumberFilter(
        method="filter_zone",
        field_name="pk",
        label=_("Security Zone (ID)"),
    )

    class Meta:
        model = AddressAssignment
        fields = ("id", "address_id", "assigned_object_type", "assigned_object_id")

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

    def filter_zone(self, queryset, name, value):
        if not (
            zones := SecurityZone.objects.filter(**{f"{name}__in": value})
        ).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(
                VirtualDeviceContext
            ),
            assigned_object_id__in=zones.values_list("id", flat=True),
        )
