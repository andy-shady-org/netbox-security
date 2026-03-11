import strawberry_django

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filters import NetBoxModelFilter

from netbox_security.models import (
    AddressList,
)

__all__ = ("NetBoxSecurityAddressListFilter",)


@strawberry_django.filter(AddressList, lookups=True)
class NetBoxSecurityAddressListFilter(NetBoxModelFilter):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
