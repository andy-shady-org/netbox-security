from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup

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
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    family: (
        Annotated[
            "NetBoxSecurityFamilyEnum", strawberry.lazy("netbox_security.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()
