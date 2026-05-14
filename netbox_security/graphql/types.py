from typing import Annotated, List

import strawberry
import strawberry_django

from netbox.graphql.types import NetBoxObjectType, PrimaryObjectType
from ipam.graphql.types import IPAddressType, PrefixType, IPRangeType
from tenancy.graphql.types import TenantType

from netbox_security.models import (
    CustomPrefix,
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
    NetBoxSecurityCustomPrefixFilter,
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


@strawberry_django.type(
    CustomPrefix, fields="__all__", filters=NetBoxSecurityCustomPrefixFilter
)
class NetBoxSecurityCustomPrefixType(PrimaryObjectType):
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    prefix: str | None


@strawberry_django.type(
    Address,
    exclude=["assigned_object_type", "assigned_object_id"],
    filters=NetBoxSecurityAddressFilter,
)
class NetBoxSecurityAddressType(PrimaryObjectType):
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    name: str
    identifier: str | None
    dns_name: str | None

    @strawberry_django.field(prefetch_related="assigned_object")
    def assigned_object(self) -> (
        Annotated[
            Annotated["IPAddressType", strawberry.lazy("ipam.graphql.types")]
            | Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")]
            | Annotated["IPRangeType", strawberry.lazy("ipam.graphql.types")]
            | Annotated[
                "NetBoxSecurityCustomPrefixType",
                strawberry.lazy("netbox_security.graphql.types"),
            ],
            strawberry.union("AddressAssignmentType"),
        ]
        | None
    ):
        return self.assigned_object


@strawberry_django.type(
    AddressSet, fields="__all__", filters=NetBoxSecurityAddressSetFilter
)
class NetBoxSecurityAddressSetType(PrimaryObjectType):
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    name: str
    identifier: str | None
    addresses: List[
        Annotated[
            "NetBoxSecurityAddressType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
    ]
    address_sets: List[
        Annotated[
            "NetBoxSecurityAddressSetType",
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
class NetBoxSecurityApplicationItemType(PrimaryObjectType):
    name: str
    index: int
    protocol: List[str] | None
    destination_ports: List[int] | None
    source_ports: List[int] | None


@strawberry_django.type(
    Application, fields="__all__", filters=NetBoxSecurityApplicationFilter
)
class NetBoxSecurityApplicationType(PrimaryObjectType):
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
class NetBoxSecurityApplicationSetType(PrimaryObjectType):
    name: str
    identifier: str | None
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    applications: List[
        Annotated[
            "NetBoxSecurityApplicationType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
    ]
    application_sets: List[
        Annotated[
            "NetBoxSecurityApplicationSetType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
    ]


@strawberry_django.type(
    SecurityZone, fields="__all__", filters=NetBoxSecuritySecurityZoneFilter
)
class NetBoxSecuritySecurityZoneType(PrimaryObjectType):
    name: str
    identifier: str | None
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None


@strawberry_django.type(
    SecurityZonePolicy, fields="__all__", filters=NetBoxSecuritySecurityZonePolicyFilter
)
class NetBoxSecuritySecurityZonePolicyType(PrimaryObjectType):
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
class NetBoxSecurityNatPoolType(PrimaryObjectType):
    name: str
    pool_type: str
    status: str


@strawberry_django.type(
    NatPoolMember, fields="__all__", filters=NetBoxSecurityNatPoolMemberFilter
)
class NetBoxSecurityNatPoolMemberType(PrimaryObjectType):
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
class NetBoxSecurityNatRuleSetType(PrimaryObjectType):
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
class NetBoxSecurityNatRuleType(PrimaryObjectType):
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
class NetBoxSecurityPolicerType(PrimaryObjectType):
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    name: str


@strawberry_django.type(
    FirewallFilter, fields="__all__", filters=NetBoxSecurityFirewallFilterFilter
)
class NetBoxSecurityFirewallFilterType(PrimaryObjectType):
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    name: str
    family: str


@strawberry_django.type(
    FirewallFilterRule, fields="__all__", filters=NetBoxSecurityFirewallFilterRuleFilter
)
class NetBoxSecurityFirewallFilterRuleType(PrimaryObjectType):
    firewall_filter: (
        Annotated[
            "NetBoxSecurityFirewallFilterType",
            strawberry.lazy("netbox_security.graphql.types"),
        ]
        | None
    )
    name: str
    index: int
