import django_filters
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.filtersets import TenancyFilterSet
from utilities.filters import (
    ContentTypeFilter,
    MultiValueCharFilter,
    MultiValueNumberFilter,
)

from dcim.models import Device, VirtualDeviceContext, Interface

from netbox_security.models import (
    SecurityZone,
    SecurityZoneAssignment,
)


class SecurityZoneFilterSet(TenancyFilterSet, NetBoxModelFilterSet):

    class Meta:
        model = SecurityZone
        fields = ["id", "name", "description"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(description__icontains=value)
        return queryset.filter(qs_filter)


class SecurityZoneAssignmentFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()
    zone_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        label=_("Security Zone (ID)"),
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
    interface = MultiValueCharFilter(
        method="filter_interface",
        field_name="name",
        label=_("Interface (name)"),
    )
    interface_id = MultiValueNumberFilter(
        method="filter_interface",
        field_name="pk",
        label=_("Interface (ID)"),
    )

    class Meta:
        model = SecurityZoneAssignment
        fields = ("id", "zone_id", "assigned_object_type", "assigned_object_id")

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

    def filter_interface(self, queryset, name, value):
        interfaces = Interface.objects.filter(**{f"{name}__in": value})
        if not interfaces.exists():
            return queryset.none()
        interface_ids = []
        interface_ids.extend(
            Interface.objects.filter(**{f"{name}__in": value}).values_list(
                "id", flat=True
            )
        )
        return queryset.filter(
            Q(
                assigned_object_type=ContentType.objects.get_for_model(Interface),
                assigned_object_id__in=interface_ids,
            )
        )
