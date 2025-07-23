import django_filters
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.filtersets import TenancyFilterSet

from netbox_security.models import (
    ApplicationSet,
    Application,
    ApplicationSetAssignment,
    SecurityZonePolicy,
)
from netbox_security.mixins import (
    AssignmentFilterSet,
)


class ApplicationSetFilterSet(TenancyFilterSet, NetBoxModelFilterSet):
    applications_id = django_filters.ModelMultipleChoiceFilter(
        field_name="applications",
        queryset=Application.objects.all(),
        to_field_name="id",
        label=_("Application (ID)"),
    )
    applications = django_filters.ModelMultipleChoiceFilter(
        field_name="applications__name",
        queryset=Application.objects.all(),
        to_field_name="name",
        label=_("Application (name)"),
    )
    application_sets_id = django_filters.ModelMultipleChoiceFilter(
        field_name="application_sets",
        queryset=ApplicationSet.objects.all(),
        to_field_name="id",
        label=_("Application Set (name)"),
    )
    application_sets = django_filters.ModelMultipleChoiceFilter(
        field_name="application_sets__name",
        queryset=ApplicationSet.objects.all(),
        to_field_name="name",
        label=_("Application Set (name)"),
    )
    security_zone_policy_id = django_filters.ModelMultipleChoiceFilter(
        field_name="securityzonepolicy_application_sets",
        queryset=SecurityZonePolicy.objects.all(),
        to_field_name="id",
    )
    application_id = django_filters.ModelMultipleChoiceFilter(
        field_name="applications",
        queryset=Application.objects.all(),
        to_field_name="id",
        label=_("Application (ID)"),
    )
    application_set_id = django_filters.ModelMultipleChoiceFilter(
        field_name="application_sets",
        queryset=ApplicationSet.objects.all(),
        to_field_name="id",
        label=_("Application Set (ID)"),
    )

    class Meta:
        model = ApplicationSet
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


class ApplicationSetAssignmentFilterSet(AssignmentFilterSet):
    application_set_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ApplicationSet.objects.all(),
        label=_("Application Set (ID)"),
    )
    application_set = django_filters.ModelMultipleChoiceFilter(
        field_name="application_set__name",
        queryset=ApplicationSet.objects.all(),
        to_field_name="name",
        label=_("Application Set (Name)"),
    )

    class Meta:
        model = ApplicationSetAssignment
        fields = (
            "id",
            "application_set_id",
            "assigned_object_type",
            "assigned_object_id",
        )
