from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from django.utils.translation import gettext_lazy as _

from utilities.filters import (
    MultiValueCharFilter,
)
from netbox_security.models import (
    ApplicationItem,
)

from netbox_security.mixins import PortsFilterSet


class ApplicationItemFilterSet(PortsFilterSet, NetBoxModelFilterSet):
    protocol = MultiValueCharFilter(
        method="filter_protocol",
        label=_("Protocols"),
    )

    class Meta:
        model = ApplicationItem
        fields = [
            "id",
            "name",
            "description",
            "index",
        ]

    def filter_protocol(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(protocol__overlap=value)

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(description__icontains=value)
        return queryset.filter(qs_filter)
