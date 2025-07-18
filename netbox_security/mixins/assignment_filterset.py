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

        if not hasattr(self, "groups"):
            setattr(self, "groups", {})

        if not self.groups:
            return base_queryset

        query = Q()
        for key in self.groups.keys():
            for name, value in self.groups[key].items():
                query |= self.filter_or(
                    base_queryset,
                    name,
                    value,
                    vdc=True if key == "virtual_devices" else False,
                )
        return base_queryset.filter(query)

    @staticmethod
    def filter_or(queryset, name, value, vdc=False):
        if vdc:
            if (
                devices := VirtualDeviceContext.objects.filter(**{f"{name}__in": value})
            ).exists():
                return Q(
                    assigned_object_type=ContentType.objects.get_for_model(
                        VirtualDeviceContext
                    ),
                    assigned_object_id__in=devices.values_list("id", flat=True),
                )
        else:
            if (devices := Device.objects.filter(**{f"{name}__in": value})).exists():
                return Q(
                    assigned_object_type=ContentType.objects.get_for_model(Device),
                    assigned_object_id__in=devices.values_list("id", flat=True),
                )
        return queryset.none()

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
