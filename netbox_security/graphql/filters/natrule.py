from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup
from strawberry.scalars import ID

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin
from ipam.graphql.filters import IPAddressFilter, IPRangeFilter, PrefixFilter

from netbox_security.graphql.enums import (
    NetBoxSecurityRuleStatusEnum,
    NetBoxSecurityCustomInterfaceEnum,
    NetBoxSecurityAddressTypeEnum,
)

from netbox_security.models import (
    NatRule,
)

from .natruleset import NetBoxSecurityNatRuleSetFilter
from .natpool import NetBoxSecurityNatPoolFilter

__all__ = ("NetBoxSecurityNatRuleFilter",)


@strawberry_django.filter(NatRule, lookups=True)
class NetBoxSecurityNatRuleFilter(ContactFilterMixin, PrimaryModelFilter):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    rule_set: (
        Annotated[
            "NetBoxSecurityNatRuleSetFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    rule_set_id: ID | None = strawberry_django.filter_field()
    pool: (
        Annotated[
            "NetBoxSecurityNatPoolFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    pool_id: ID | None = strawberry_django.filter_field()
    source_pool: (
        Annotated[
            "NetBoxSecurityNatPoolFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    source_pool_id: ID | None = strawberry_django.filter_field()
    destination_pool: (
        Annotated[
            "NetBoxSecurityNatPoolFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    destination_pool_id: ID | None = strawberry_django.filter_field()
    status: (
        Annotated[
            "NetBoxSecurityRuleStatusEnum",
            strawberry.lazy("netbox_security.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()
    source_type: (
        Annotated[
            "NetBoxSecurityAddressTypeEnum",
            strawberry.lazy("netbox_security.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()
    destination_type: (
        Annotated[
            "NetBoxSecurityAddressTypeEnum",
            strawberry.lazy("netbox_security.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()
    source_addresses: (
        Annotated["IPAddressFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    destination_addresses: (
        Annotated["IPAddressFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    source_prefixes: (
        Annotated["PrefixFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    destination_prefixes: (
        Annotated["PrefixFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    source_ranges: (
        Annotated["IPRangeFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    destination_ranges: (
        Annotated["IPRangeFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    custom_interface: (
        Annotated[
            "NetBoxSecurityCustomInterfaceEnum",
            strawberry.lazy("netbox_security.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()
