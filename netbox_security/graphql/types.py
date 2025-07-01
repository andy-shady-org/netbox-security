from typing import Annotated, List

import strawberry
import strawberry_django

from netbox.graphql.types import NetBoxObjectType
from ipam.graphql.types import IPAddressType, PrefixType, IPRangeType
from tenancy.graphql.types import TenantType

from netbox_security.models import (
    Address,
    AddressSet,
    AddressList,
    ApplicationItem,
    Application,
    ApplicationSet,
    SecurityZone,
    SecurityZonePolicy,
    NatPool,
    NatPoolMember,
    NatRuleSet,
    NatRule,
    FirewallFilter,
    FirewallFilterRule,
    Policer,
)

from .filters import (
    NetBoxSecurityAddressFilter,
    NetBoxSecurityAddressSetFilter,
    NetBoxSecurityAddressListFilter,
    NetBoxSecurityApplicationItemFilter,
    NetBoxSecurityApplicationFilter,
    NetBoxSecurityApplicationSetFilter,
    NetBoxSecuritySecurityZoneFilter,
    NetBoxSecuritySecurityZonePolicyFilter,
    NetBoxSecurityNatPoolFilter,
    NetBoxSecurityNatPoolMemberFilter,
    NetBoxSecurityNatRuleSetFilter,
    NetBoxSecurityNatRuleFilter,
    NetBoxSecurityPolicerFilter,
    NetBoxSecurityFirewallFilterFilter,
    NetBoxSecurityFirewallFilterRuleFilter,
)


@strawberry_django.type(Address, fields="__all__", filters=NetBoxSecurityAddressFilter)
class NetBoxSecurityAddressType(NetBoxObjectType):
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    name: str
    identifier: str | None
    address: str | None
    dns_name: str | None
    ip_range: Annotated["IPRangeType", strawberry.lazy("ipam.graphql.types")] | None


@strawberry_django.type(
    AddressSet, fields="__all__", filters=NetBoxSecurityAddressSetFilter
)
class NetBoxSecurityAddressSetType(NetBoxObjectType):
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    name: str
    identifier: str | None
    addresses: List[
        Annotated[
            "NetBoxSecurityAddressType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
    ]


@strawberry_django.type(
    AddressList, fields="__all__", filters=NetBoxSecurityAddressListFilter
)
class NetBoxSecurityAddressListType(NetBoxObjectType):
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    name: str
    value: str


@strawberry_django.type(
    ApplicationItem, fields="__all__", filters=NetBoxSecurityApplicationItemFilter
)
class NetBoxSecurityApplicationItemType(NetBoxObjectType):
    name: str
    index: int
    protocol: List[str] | None
    destination_ports: List[int] | None
    source_ports: List[int] | None


@strawberry_django.type(
    Application, fields="__all__", filters=NetBoxSecurityApplicationFilter
)
class NetBoxSecurityApplicationType(NetBoxObjectType):
    name: str
    identifier: str | None
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    application_items: List[
        Annotated[
            "NetBoxSecurityApplicationItemType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
    ]
    protocol: List[str] | None
    destination_ports: List[int] | None
    source_ports: List[int] | None


@strawberry_django.type(
    ApplicationSet, fields="__all__", filters=NetBoxSecurityApplicationSetFilter
)
class NetBoxSecurityApplicationSetType(NetBoxObjectType):
    name: str
    identifier: str | None
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    applications: List[
        Annotated[
            "NetBoxSecurityApplicationType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
    ]


@strawberry_django.type(
    SecurityZone, fields="__all__", filters=NetBoxSecuritySecurityZoneFilter
)
class NetBoxSecuritySecurityZoneType(NetBoxObjectType):
    name: str
    identifier: str | None
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None


@strawberry_django.type(
    SecurityZonePolicy, fields="__all__", filters=NetBoxSecuritySecurityZonePolicyFilter
)
class NetBoxSecuritySecurityZonePolicyType(NetBoxObjectType):
    name: str
    identifier: str | None
    source_zone: (
        Annotated[
            "NetBoxSecuritySecurityZoneType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
        | None
    )
    destination_zone: (
        Annotated[
            "NetBoxSecuritySecurityZoneType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
        | None
    )
    source_address: (
        List[
            Annotated[
                "NetBoxSecurityAddressType",
                strawberry.lazy("netbox_security.graphql.types"),
            ]
        ]
        | None
    )
    destination_address: (
        List[
            Annotated[
                "NetBoxSecurityAddressType",
                strawberry.lazy("netbox_security.graphql.types"),
            ]
        ]
        | None
    )


@strawberry_django.type(NatPool, fields="__all__", filters=NetBoxSecurityNatPoolFilter)
class NetBoxSecurityNatPoolType(NetBoxObjectType):
    name: str
    pool_type: str
    status: str


@strawberry_django.type(
    NatPoolMember, fields="__all__", filters=NetBoxSecurityNatPoolMemberFilter
)
class NetBoxSecurityNatPoolMemberType(NetBoxObjectType):
    pool: (
        Annotated[
            "NetBoxSecurityNatPoolType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
        | None
    )
    address: Annotated["IPAddressType", strawberry.lazy("ipam.graphql.types")] | None
    prefix: Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")] | None
    address_range: (
        Annotated["IPRangeType", strawberry.lazy("ipam.graphql.types")] | None
    )
    status: str
    name: str


@strawberry_django.type(
    NatRuleSet, fields="__all__", filters=NetBoxSecurityNatRuleSetFilter
)
class NetBoxSecurityNatRuleSetType(NetBoxObjectType):
    source_zones: List[
        Annotated[
            "NetBoxSecuritySecurityZoneType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
    ]
    destination_zones: List[
        Annotated[
            "NetBoxSecuritySecurityZoneType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
    ]
    name: str
    nat_type: str
    direction: str


@strawberry_django.type(NatRule, fields="__all__", filters=NetBoxSecurityNatRuleFilter)
class NetBoxSecurityNatRuleType(NetBoxObjectType):
    rule_set: (
        Annotated[
            "NetBoxSecurityNatRuleSetType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
        | None
    )
    pool: (
        Annotated[
            "NetBoxSecurityNatPoolType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
        | None
    )
    source_addresses: (
        List[Annotated["IPAddressType", strawberry.lazy("ipam.graphql.types")]] | None
    )
    destination_addresses: (
        List[Annotated["IPAddressType", strawberry.lazy("ipam.graphql.types")]] | None
    )
    source_prefixes: (
        List[Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")]] | None
    )
    destination_prefixes: (
        List[Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")]] | None
    )
    source_ranges: (
        List[Annotated["IPRangeType", strawberry.lazy("ipam.graphql.types")]] | None
    )
    destination_ranges: (
        List[Annotated["IPRangeType", strawberry.lazy("ipam.graphql.types")]] | None
    )
    source_pool: (
        Annotated[
            "NetBoxSecurityNatPoolType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
        | None
    )
    destination_pool: (
        Annotated[
            "NetBoxSecurityNatPoolType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
        | None
    )
    status: str
    source_type: str
    destination_type: str
    source_ports: List[int] | None
    destination_ports: List[int] | None


@strawberry_django.type(Policer, fields="__all__", filters=NetBoxSecurityPolicerFilter)
class NetBoxSecurityPolicerType(NetBoxObjectType):
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    name: str


@strawberry_django.type(
    FirewallFilter, fields="__all__", filters=NetBoxSecurityFirewallFilterFilter
)
class NetBoxSecurityFirewallFilterType(NetBoxObjectType):
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    name: str
    family: str


@strawberry_django.type(
    FirewallFilterRule, fields="__all__", filters=NetBoxSecurityFirewallFilterRuleFilter
)
class NetBoxSecurityFirewallFilterRuleType(NetBoxObjectType):
    firewall_filter: (
        Annotated[
            "NetBoxSecurityFirewallFilterType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
        | None
    )
    name: str
    index: int
