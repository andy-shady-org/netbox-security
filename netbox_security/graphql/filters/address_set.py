from typing import Annotated, List
import strawberry
import strawberry_django
from strawberry_django import FilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin, TenancyFilterMixin

from netbox_security.models import (
    AddressSet,
)
from .address import NetBoxSecurityAddressFilter

__all__ = ("NetBoxSecurityAddressSetFilter",)


@strawberry_django.filter(AddressSet, lookups=True)
class NetBoxSecurityAddressSetFilter(
    ContactFilterMixin, TenancyFilterMixin, PrimaryModelFilter
):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    identifier: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    addresses: (
        Annotated[
            "NetBoxSecurityAddressFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    address_sets: (
        Annotated[
            "NetBoxSecurityAddressSetFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
