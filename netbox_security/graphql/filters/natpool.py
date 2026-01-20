from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from ipam.graphql.enums import IPAddressStatusEnum
from tenancy.graphql.filter_mixins import ContactFilterMixin

from netbox_security.graphql.enums import (
    NetBoxSecurityPoolTypeEnum,
)

from netbox_security.models import (
    NatPool,
)

__all__ = ("NetBoxSecurityNatPoolFilter",)


@strawberry_django.filter(NatPool, lookups=True)
class NetBoxSecurityNatPoolFilter(ContactFilterMixin, PrimaryModelFilter):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    pool_type: (
        Annotated[
            "NetBoxSecurityPoolTypeEnum",
            strawberry.lazy("netbox_security.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()
    status: (
        Annotated["IPAddressStatusEnum", strawberry.lazy("ipam.graphql.enums")] | None
    ) = strawberry_django.filter_field()
