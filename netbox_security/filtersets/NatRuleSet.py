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
from dcim.models import Device

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
    source_zones = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all()
    )
    destination_zones = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all()
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

    class Meta:
        model = NatRuleSetAssignment
        fields = ("id", "ruleset_id", "assigned_object_type", "assigned_object_id")

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
