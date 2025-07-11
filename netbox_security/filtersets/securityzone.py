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
    NatRuleSet,
)


class SecurityZoneFilterSet(TenancyFilterSet, NetBoxModelFilterSet):
    source_zone_id = django_filters.ModelMultipleChoiceFilter(
        field_name="natruleset_source_zones",
        queryset=SecurityZone.objects.all(),
        to_field_name="id",
        label=_("Source Zone NAT Rule Set (ID)"),
    )
    destination_zone_id = django_filters.ModelMultipleChoiceFilter(
        field_name="natruleset_destination_zones",
        queryset=SecurityZone.objects.all(),
        to_field_name="id",
        label=_("Destination Zone NAT Rule Set (ID)"),
    )
    nat_rule_set_id = django_filters.ModelMultipleChoiceFilter(
        method="filter_natruleset",
        queryset=NatRuleSet.objects.all(),
        label=_("NAT Rule Set (ID)"),
    )

    class Meta:
        model = SecurityZone
        fields = ["id", "name", "description", "identifier"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(identifier__icontains=value)
        )
        return queryset.filter(qs_filter)

    def filter_natruleset(self, queryset, name, value):
        """Filter NAT Rule Set (ID)."""
        if not value:
            return queryset
        rules = {rule.pk for rule in value}
        qs_filter = Q(natruleset_destination_zones__id__in=rules) | Q(
            natruleset_source_zones__id__in=rules
        )
        return queryset.filter(qs_filter)


class SecurityZoneAssignmentFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()
    zone_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        label=_("Security Zone (ID)"),
    )
    zone = django_filters.ModelMultipleChoiceFilter(
        field_name="zone__name",
        queryset=SecurityZone.objects.all(),
        to_field_name="name",
        label=_("Security Zone (Name)"),
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

    def filter_interface(self, queryset, name, value):
        if not (
            interfaces := Interface.objects.filter(**{f"{name}__in": value})
        ).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(Interface),
            assigned_object_id__in=interfaces.values_list("id", flat=True),
        )
