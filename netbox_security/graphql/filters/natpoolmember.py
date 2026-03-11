from typing import Annotated
import strawberry
import strawberry_django
from strawberry.scalars import ID

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from ipam.graphql.enums import IPAddressStatusEnum
from ipam.graphql.filters import IPAddressFilter, IPRangeFilter, PrefixFilter
from netbox_security.models import (
    NatPoolMember,
)

from .natpool import NetBoxSecurityNatPoolFilter

__all__ = ("NetBoxSecurityNatPoolMemberFilter",)


@strawberry_django.filter(NatPoolMember, lookups=True)
class NetBoxSecurityNatPoolMemberFilter(PrimaryModelFilter):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()
    pool: (
        Annotated[
            "NetBoxSecurityNatPoolFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    pool_id: ID | None = strawberry_django.filter_field()
    status: (
        Annotated["IPAddressStatusEnum", strawberry.lazy("ipam.graphql.enums")] | None
    ) = strawberry_django.filter_field()
    address: (
        Annotated["IPAddressFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    address_id: ID | None = strawberry_django.filter_field()
    prefix: (
        Annotated["PrefixFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    prefix_id: ID | None = strawberry_django.filter_field()
    address_range: (
        Annotated["IPRangeFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    address_range_id: ID | None = strawberry_django.filter_field()
