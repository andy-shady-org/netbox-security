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
from ipam.models import IPRange, Prefix, IPAddress
from virtualization.models import VirtualMachine

from netbox_security.models import (
    Address,
    CustomPrefix,
    AddressSet,
    AddressAssignment,
    SecurityZone,
)
from netbox_security.mixins import (
    AssignmentFilterSet,
)

__all__ = (
    "AddressFilterSet",
    "AddressAssignmentFilterSet",
)


@register_filterset
class AddressFilterSet(TenancyFilterSet, PrimaryModelFilterSet):
    assigned_object_id = MultiValueNumberFilter(
        field_name="assigned_object_id",
        label=_("Assigned Object (ID)"),
    )
    assigned_object_type_id = django_filters.ModelMultipleChoiceFilter(
        field_name="assigned_object_type",
        queryset=ContentType.objects.all(),
        to_field_name="id",
        label=_("Assigned Object Type (ID)"),
    )
    assigned_object_type = django_filters.ModelMultipleChoiceFilter(
        field_name="assigned_object_type__model",
        queryset=ContentType.objects.all(),
        to_field_name="model",
        label=_("Assigned Object Type (Model)"),
    )
    address_set_id = django_filters.ModelMultipleChoiceFilter(
        queryset=AddressSet.objects.all(),
        field_name="addressset_addresses",
        to_field_name="id",
        label=_("Address Set (ID)"),
    )
    custom_prefix_id = django_filters.ModelMultipleChoiceFilter(
        field_name="custom_prefixes",
        queryset=CustomPrefix.objects.all(),
        label=_("Custom Prefix (ID)"),
    )
    custom_prefix = django_filters.ModelMultipleChoiceFilter(
        field_name="custom_prefixes__prefix",
        queryset=CustomPrefix.objects.all(),
        to_field_name="prefix",
        label=_("Custom Prefix (Prefix)"),
    )
    # Aliases for reverse GenericRelation field names used by filter coverage tests.
    custom_prefixes = django_filters.ModelMultipleChoiceFilter(
        field_name="custom_prefixes",
        queryset=CustomPrefix.objects.all(),
        label=_("Custom Prefixes"),
    )
    prefix_id = django_filters.ModelMultipleChoiceFilter(
        field_name="prefixes",
        queryset=Prefix.objects.all(),
        label=_("Prefix (ID)"),
    )
    prefix = django_filters.ModelMultipleChoiceFilter(
        field_name="prefixes__prefix",
        queryset=Prefix.objects.all(),
        to_field_name="prefix",
        label=_("Prefix (Name)"),
    )
    prefixes = django_filters.ModelMultipleChoiceFilter(
        field_name="prefixes",
        queryset=Prefix.objects.all(),
        label=_("Prefixes"),
    )
    ip_address_id = django_filters.ModelMultipleChoiceFilter(
        field_name="ip_addresses",
        queryset=IPAddress.objects.all(),
        label=_("IP Address (ID)"),
    )
    ip_address = django_filters.ModelMultipleChoiceFilter(
        field_name="ip_addresses__address",
        queryset=IPAddress.objects.all(),
        to_field_name="address",
        label=_("IP Address (Address)"),
    )
    ip_addresses = django_filters.ModelMultipleChoiceFilter(
        field_name="ip_addresses",
        queryset=IPAddress.objects.all(),
        label=_("IP Addresses"),
    )
    ip_range_id = django_filters.ModelMultipleChoiceFilter(
        field_name="ip_ranges",
        queryset=IPRange.objects.all(),
        to_field_name="id",
        label=_("IPRange (ID)"),
    )
    ip_range = django_filters.ModelMultipleChoiceFilter(
        field_name="ip_ranges__start_address",
        queryset=IPRange.objects.all(),
        to_field_name="start_address",
        label=_("IPRange (Start Address)"),
    )
    ip_ranges = django_filters.ModelMultipleChoiceFilter(
        field_name="ip_ranges",
        queryset=IPRange.objects.all(),
        label=_("IP Ranges"),
    )

    class Meta:
        model = Address
        fields = ["id", "name", "description", "dns_name", "identifier"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(identifier__icontains=value)
            | Q(dns_name=value)
        )
        return queryset.filter(qs_filter)


@register_filterset
class AddressAssignmentFilterSet(AssignmentFilterSet):
    address_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Address.objects.all(),
        label=_("Address (ID)"),
    )
    address = django_filters.ModelMultipleChoiceFilter(
        field_name="address__name",
        queryset=Address.objects.all(),
        to_field_name="name",
        label=_("Address (Name)"),
    )
    security_zone = MultiValueCharFilter(
        method="filter_zone",
        field_name="name",
        label=_("Security Zone (name)"),
    )
    security_zone_id = MultiValueNumberFilter(
        method="filter_zone",
        field_name="pk",
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
        method="filter_virtualdevicecontext",
        field_name="name",
        label=_("Virtual Device Context (name)"),
    )
    virtualdevicecontext_id = MultiValueNumberFilter(
        method="filter_virtualdevicecontext",
        field_name="pk",
        label=_("Virtual Device Context (ID)"),
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
        model = AddressAssignment
        fields = ("id", "address_id", "assigned_object_type", "assigned_object_id")

    def filter_zone(self, queryset, name, value):
        if not (
            zones := SecurityZone.objects.filter(**{f"{name}__in": value})
        ).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(SecurityZone),
            assigned_object_id__in=zones.values_list("id", flat=True),
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

    def filter_virtual_machine(self, queryset, name, value):
        if not (
            devices := VirtualMachine.objects.filter(**{f"{name}__in": value})
        ).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(VirtualMachine),
            assigned_object_id__in=devices.values_list("id", flat=True),
        )
