import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from netbox_security.models import (
    ApplicationItem,
)
from netbox_security.choices import ProtocolChoices


class ApplicationItemFilterSet(NetBoxModelFilterSet):
    protocol = django_filters.MultipleChoiceFilter(
        choices=ProtocolChoices,
        required=False,
    )

    class Meta:
        model = ApplicationItem
        fields = [
            "id",
            "name",
            "description",
            "index",
            "destination_port",
            "source_port",
        ]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(description__icontains=value)
        return queryset.filter(qs_filter)
