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


class AssignmentFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()
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

    @property
    def qs(self):
        base_queryset = super().qs

        groups = getattr(self, "groups", {})
        if not groups:
            return base_queryset

        combined_query = Q()
        for group_key, filters in groups.items():
            is_vdc = group_key == "virtual_devices"
            for field, values in filters.items():
                combined_query |= self._build_device_filter(field, values, is_vdc)

        return base_queryset.filter(combined_query)

    @staticmethod
    def _build_device_filter(field, values, is_vdc=False):
        model = VirtualDeviceContext if is_vdc else Device
        content_type = ContentType.objects.get_for_model(model)

        devices = model.objects.filter(**{f"{field}__in": values}).values_list(
            "id", flat=True
        )
        if devices.exists():
            return Q(assigned_object_type=content_type, assigned_object_id__in=devices)

        return Q(pk__in=[])  # Return empty Q instead of queryset.none()

    def filter_device(self, queryset, name, value):
        if not hasattr(self, "groups"):
            setattr(self, "groups", {})
        self.groups["devices"] = {}
        if not Device.objects.filter(**{f"{name}__in": value}).exists():
            return queryset.none()
        self.groups["devices"][name] = value
        return queryset

    def filter_context(self, queryset, name, value):
        if not hasattr(self, "groups"):
            setattr(self, "groups", {})
        self.groups["virtual_devices"] = {}
        if not VirtualDeviceContext.objects.filter(**{f"{name}__in": value}).exists():
            return queryset.none()
        self.groups["virtual_devices"][name] = value
        return queryset
