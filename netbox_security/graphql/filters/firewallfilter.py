from typing import Annotated
import strawberry
import strawberry_django

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin, TenancyFilterMixin

from netbox_security.graphql.enums import (
    NetBoxSecurityFamilyEnum,
)

from netbox_security.models import (
    FirewallFilter,
)

__all__ = ("NetBoxSecurityFirewallFilterFilter",)


@strawberry_django.filter(FirewallFilter, lookups=True)
class NetBoxSecurityFirewallFilterFilter(
    ContactFilterMixin, TenancyFilterMixin, PrimaryModelFilter
):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()
    family: (
        Annotated[
            "NetBoxSecurityFamilyEnum", strawberry.lazy("netbox_security.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()
