import django_filters
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils.translation import gettext as _

from netbox.filtersets import PrimaryModelFilterSet
from utilities.filtersets import register_filterset
from utilities.filters import MultiValueCharFilter, MultiValueNumberFilter

from netbox_security.choices import (
    FirewallRuleFromSettingChoices,
    FirewallRuleThenSettingChoices,
)
from netbox_security.models import (
    FirewallFilterRule,
    FirewallFilter,
    FirewallRuleFromSetting,
    FirewallRuleThenSetting,
)

__all__ = (
    "FirewallFilterRuleFilterSet",
    "FirewallRuleFromSettingFilterSet",
    "FirewallRuleThenSettingFilterSet",
)


@register_filterset
class FirewallFilterRuleFilterSet(PrimaryModelFilterSet):
    firewall_filter_id = django_filters.ModelMultipleChoiceFilter(
        queryset=FirewallFilter.objects.all(),
        field_name="firewall_filter",
        to_field_name="id",
        label=_("Firewall Filter (ID)"),
    )
    firewall_filter = django_filters.ModelMultipleChoiceFilter(
        queryset=FirewallFilter.objects.all(),
        field_name="firewall_filter__name",
        to_field_name="name",
        label=_("Firewall Filter (Name)"),
    )

    class Meta:
        model = FirewallFilterRule
        fields = ["id", "name", "description", "index"]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(description__icontains=value)
        return queryset.filter(qs_filter).distinct()


@register_filterset
class FirewallRuleFromSettingFilterSet(PrimaryModelFilterSet):
    assigned_object_id = MultiValueNumberFilter(
        field_name="assigned_object_id",
        label=_("Assigned Object ID"),
    )
    key = django_filters.MultipleChoiceFilter(
        choices=FirewallRuleFromSettingChoices, null_value=None, label=_("Setting Name")
    )
    value = MultiValueCharFilter(
        field_name="value",
        label=_("Value"),
    )
    firewall_filter_rule_id = django_filters.ModelMultipleChoiceFilter(
        queryset=FirewallFilterRule.objects.all(),
        method="filter_firewall_filter_rule_id",
        label=_("Firewall Filter Rule (ID)"),
    )

    class Meta:
        model = FirewallRuleFromSetting
        fields = [
            "id",
            "assigned_object_id",
            "key",
            "value",
            "description",
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(key__icontains=value) | Q(value__icontains=value)
        return queryset.filter(qs_filter).distinct()

    def filter_firewall_filter_rule_id(self, queryset, name, value):
        if not value:
            return queryset

        rule_ct = ContentType.objects.get_for_model(FirewallFilterRule)
        return queryset.filter(
            assigned_object_type=rule_ct,
            assigned_object_id__in=[rule.pk for rule in value],
        )


@register_filterset
class FirewallRuleThenSettingFilterSet(PrimaryModelFilterSet):
    assigned_object_id = MultiValueNumberFilter(
        field_name="assigned_object_id",
        label=_("Assigned Object ID"),
    )
    key = django_filters.MultipleChoiceFilter(
        choices=FirewallRuleThenSettingChoices, null_value=None, label=_("Setting Name")
    )
    value = MultiValueCharFilter(
        field_name="value",
        label=_("Value"),
    )
    firewall_filter_rule_id = django_filters.ModelMultipleChoiceFilter(
        queryset=FirewallFilterRule.objects.all(),
        method="filter_firewall_filter_rule_id",
        label=_("Firewall Filter Rule (ID)"),
    )

    class Meta:
        model = FirewallRuleThenSetting
        fields = [
            "id",
            "assigned_object_id",
            "key",
            "value",
            "description",
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(key__icontains=value) | Q(value__icontains=value)
        return queryset.filter(qs_filter).distinct()

    def filter_firewall_filter_rule_id(self, queryset, name, value):
        if not value:
            return queryset

        rule_ct = ContentType.objects.get_for_model(FirewallFilterRule)
        return queryset.filter(
            assigned_object_type=rule_ct,
            assigned_object_id__in=[rule.pk for rule in value],
        )
