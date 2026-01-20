import strawberry_django
from strawberry_django import FilterLookup

from netbox.graphql.filters import NetBoxModelFilter

from netbox_security.models import (
    AddressList,
)

__all__ = ("NetBoxSecurityAddressListFilter",)


@strawberry_django.filter(AddressList, lookups=True)
class NetBoxSecurityAddressListFilter(NetBoxModelFilter):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
