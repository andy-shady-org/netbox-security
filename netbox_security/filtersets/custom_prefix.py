from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from netaddr import IPNetwork
from netaddr.core import AddrFormatError
from netbox.filtersets import PrimaryModelFilterSet
from tenancy.filtersets import TenancyFilterSet
from utilities.filtersets import register_filterset
from utilities.filters import MultiValueCharFilter

from netbox_security.models import (
    CustomPrefix,
)

__all__ = ("CustomPrefixFilterSet",)


@register_filterset
class CustomPrefixFilterSet(TenancyFilterSet, PrimaryModelFilterSet):
    prefix = MultiValueCharFilter(
        method="filter_prefix",
        label=_("Prefix"),
    )

    class Meta:
        model = CustomPrefix
        fields = [
            "id",
            "prefix",
            "description",
        ]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(description__icontains=value)
        return queryset.filter(qs_filter)

    def filter_prefix(self, queryset, name, value):
        # value is a list of prefix strings from MultiValueCharFilter
        normalized = []
        for v in value:
            try:
                normalized.append(str(IPNetwork(v).cidr))
            except (AddrFormatError, ValueError):
                pass
        if not normalized:
            return queryset.none()
        return queryset.filter(prefix__in=normalized)
