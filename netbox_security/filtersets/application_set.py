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

from netbox_security.models import (
    ApplicationSet,
    Application,
    ApplicationSetAssignment,
    SecurityZonePolicy,
)
from netbox_security.mixins import (
    AssignmentFilterSet,
)

__all__ = (
    "ApplicationSetFilterSet",
    "ApplicationSetAssignmentFilterSet",
)


@register_filterset
class ApplicationSetFilterSet(TenancyFilterSet, PrimaryModelFilterSet):
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


@register_filterset
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

    class Meta:
        model = ApplicationSetAssignment
        fields = (
            "id",
            "application_set_id",
            "assigned_object_type",
            "assigned_object_id",
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
