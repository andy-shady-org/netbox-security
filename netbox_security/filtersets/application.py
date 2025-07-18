import django_filters
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.filtersets import TenancyFilterSet
from utilities.filters import (
    MultiValueCharFilter,
)


from netbox_security.models import (
    Application,
    ApplicationSet,
    ApplicationAssignment,
    ApplicationItem,
    SecurityZonePolicy,
)

from netbox_security.mixins import PortsFilterSet, AssignmentFilterSet


class ApplicationFilterSet(PortsFilterSet, TenancyFilterSet, NetBoxModelFilterSet):
    application_items_id = django_filters.ModelMultipleChoiceFilter(
        field_name="application_items",
        queryset=ApplicationItem.objects.all(),
        to_field_name="id",
        label=_("Application Item (ID)"),
    )
    application_items = django_filters.ModelMultipleChoiceFilter(
        field_name="application_items__name",
        queryset=ApplicationItem.objects.all(),
        to_field_name="name",
        label=_("Application Item (name)"),
    )
    protocol = MultiValueCharFilter(
        method="filter_protocol",
        label=_("Protocols"),
    )
    security_zone_policy_id = django_filters.ModelMultipleChoiceFilter(
        field_name="securityzonepolicy_applications",
        queryset=SecurityZonePolicy.objects.all(),
        to_field_name="id",
    )
    application_item_id = django_filters.ModelMultipleChoiceFilter(
        field_name="application_items",
        queryset=ApplicationItem.objects.all(),
        to_field_name="id",
        label=_("Application (ID)"),
    )
    application_set_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ApplicationSet.objects.all(),
        field_name="applicationset_applications",
        to_field_name="id",
        label=_("Application Set (ID)"),
    )

    class Meta:
        model = Application
        fields = ["id", "name", "description", "identifier"]

    def filter_protocol(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(protocol__overlap=value)

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


class ApplicationAssignmentFilterSet(AssignmentFilterSet):
    application_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Application.objects.all(),
        label=_("Application (ID)"),
    )
    application = django_filters.ModelMultipleChoiceFilter(
        field_name="application__name",
        queryset=Application.objects.all(),
        to_field_name="name",
        label=_("Application (Name)"),
    )

    class Meta:
        model = ApplicationAssignment
        fields = ("id", "application_id", "assigned_object_type", "assigned_object_id")
