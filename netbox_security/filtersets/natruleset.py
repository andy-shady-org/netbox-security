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
from virtualization.models import VirtualMachine

from netbox_security.models import (
    NatRuleSet,
    NatRuleSetAssignment,
    SecurityZone,
)

from netbox_security.choices import (
    RuleDirectionChoices,
    NatTypeChoices,
)


class NatRuleSetFilterSet(NetBoxModelFilterSet):
    nat_type = django_filters.MultipleChoiceFilter(
        choices=NatTypeChoices,
        required=False,
    )
    direction = django_filters.MultipleChoiceFilter(
        choices=RuleDirectionChoices,
        required=False,
    )
    source_zone_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        field_name="source_zones",
        to_field_name="id",
        label=_("Source Zone (ID)"),
    )
    source_zone = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        field_name="source_zones__name",
        to_field_name="name",
        label=_("Source Zone (Name)"),
    )
    destination_zone_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        field_name="destination_zones",
        to_field_name="id",
        label=_("Destination Zone (ID)"),
    )
    destination_zone = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        field_name="destination_zones__name",
        to_field_name="name",
        label=_("Destination Zone (Name)"),
    )
    security_zone_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        field_name="source_zones",
        to_field_name="id",
        label=_("Source Zone (ID)"),
    )

    class Meta:
        model = NatRuleSet
        fields = ["id", "name", "description"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(description__icontains=value)
        return queryset.filter(qs_filter)


class NatRuleSetAssignmentFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()
    ruleset_id = django_filters.ModelMultipleChoiceFilter(
        queryset=NatRuleSet.objects.all(),
        label=_("NAT Ruleset (ID)"),
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
        method="filter_virtual_device",
        field_name="name",
        label=_("Virtual Device Context (name)"),
    )
    virtualdevicecontext_id = MultiValueNumberFilter(
        method="filter_virtual_device",
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
        model = NatRuleSetAssignment
        fields = ("id", "ruleset_id", "assigned_object_type", "assigned_object_id")

    def filter_device(self, queryset, name, value):
        if not (devices := Device.objects.filter(**{f"{name}__in": value})).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(Device),
            assigned_object_id__in=devices.values_list("id", flat=True),
        )

    def filter_virtual_device(self, queryset, name, value):
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
