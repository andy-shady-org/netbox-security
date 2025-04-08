import django_filters
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filters import (
    ContentTypeFilter,
    MultiValueCharFilter,
    MultiValueNumberFilter,
    NumericArrayFilter,
)
from dcim.models import Device, VirtualDeviceContext
from ipam.models import IPAddress, Prefix, IPRange

from netbox_security.models import (
    NatPool,
    NatRule,
    NatRuleSet,
    NatRuleAssignment,
)

from netbox_security.choices import AddressTypeChoices, RuleStatusChoices


class NatRuleFilterSet(NetBoxModelFilterSet):
    rule_set_id = django_filters.ModelMultipleChoiceFilter(
        queryset=NatRuleSet.objects.all(),
        field_name="rule_set",
        to_field_name="id",
        label=_("Rule Set (ID)"),
    )
    rule_set = django_filters.ModelMultipleChoiceFilter(
        queryset=NatRuleSet.objects.all(),
        field_name="rule_set",
        to_field_name="name",
        label=_("Rule Set (ID)"),
    )
    pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=NatPool.objects.all(),
        field_name="pool",
        to_field_name="id",
        label=_("NAT Pool (ID)"),
    )
    pool = django_filters.ModelMultipleChoiceFilter(
        queryset=NatPool.objects.all(),
        field_name="pool",
        to_field_name="name",
        label=_("NAT Pool (Name)"),
    )
    status = django_filters.MultipleChoiceFilter(
        choices=RuleStatusChoices,
        required=False,
    )
    source_type = django_filters.MultipleChoiceFilter(
        choices=AddressTypeChoices,
        required=False,
    )
    destination_type = django_filters.MultipleChoiceFilter(
        choices=AddressTypeChoices,
        required=False,
    )
    source_addresses = django_filters.ModelMultipleChoiceFilter(
        queryset=IPAddress.objects.all(),
    )
    destination_addresses = django_filters.ModelMultipleChoiceFilter(
        queryset=IPAddress.objects.all(),
    )
    source_prefixes = django_filters.ModelMultipleChoiceFilter(
        queryset=Prefix.objects.all(),
    )
    destination_prefixes = django_filters.ModelMultipleChoiceFilter(
        queryset=Prefix.objects.all(),
    )
    destination_ranges = django_filters.ModelMultipleChoiceFilter(
        queryset=IPRange.objects.all(),
    )
    source_ranges = django_filters.ModelMultipleChoiceFilter(
        queryset=IPRange.objects.all(),
    )
    source_port = NumericArrayFilter(field_name="source_ports", lookup_expr="contains")
    destination_port = NumericArrayFilter(
        field_name="destination_ports", lookup_expr="contains"
    )
    source_pool = django_filters.ModelMultipleChoiceFilter(
        queryset=NatPool.objects.all()
    )
    destination_pool = django_filters.ModelMultipleChoiceFilter(
        queryset=NatPool.objects.all()
    )

    class Meta:
        model = NatRule
        fields = ["id", "name", "description", "custom_interface"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(custom_interface__icontains=value)
        )
        return queryset.filter(qs_filter)


class NatRuleAssignmentFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()
    rule_id = django_filters.ModelMultipleChoiceFilter(
        queryset=NatRule.objects.all(),
        label=_("NAT Rule (ID)"),
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
        model = NatRuleAssignment
        fields = ("id", "rule_id", "assigned_object_type", "assigned_object_id")

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
