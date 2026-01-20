from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup
from strawberry.scalars import ID

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
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    identifier: FilterLookup[str] | None = strawberry_django.filter_field()
    address: FilterLookup[str] | None = strawberry_django.filter_field()
    dns_name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    ip_range: (
        Annotated["IPRangeFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    ip_range_id: ID | None = strawberry_django.filter_field()
