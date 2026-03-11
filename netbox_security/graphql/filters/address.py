from typing import Annotated
import strawberry
import strawberry_django
from strawberry.scalars import ID

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup


from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin, TenancyFilterMixin
from ipam.graphql.filters import IPRangeFilter

from netbox_security.models import (
    Address,
)

__all__ = ("NetBoxSecurityAddressFilter",)


@strawberry_django.filter(Address, lookups=True)
class NetBoxSecurityAddressFilter(
    ContactFilterMixin, TenancyFilterMixin, PrimaryModelFilter
):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    identifier: StrFilterLookup[str] | None = strawberry_django.filter_field()
    address: StrFilterLookup[str] | None = strawberry_django.filter_field()
    dns_name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()
    ip_range: (
        Annotated["IPRangeFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    ip_range_id: ID | None = strawberry_django.filter_field()
