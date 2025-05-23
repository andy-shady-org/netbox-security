from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup

from netbox.graphql.filter_mixins import NetBoxModelFilterMixin
from ipam.graphql.enums import IPAddressStatusEnum
from tenancy.graphql.filter_mixins import ContactFilterMixin, TenancyFilterMixin
from ipam.graphql.filters import IPAddressFilter, IPRangeFilter, PrefixFilter

from .filter_lookups import PolicyActionArrayLookup
from .enums import (
    NetBoxSecurityFamilyEnum,
    NetBoxSecurityPoolTypeEnum,
    NetBoxSecurityRuleDirectionEnum,
    NetBoxSecurityNatTypeEnum,
    NetBoxSecurityRuleStatusEnum,
    NetBoxSecurityCustomInterfaceEnum,
    NetBoxSecurityAddressTypeEnum,
    NetBoxSecurityLossPriorityEnum,
    NetBoxSecurityForwardingClassEnum,
)

from netbox_security.models import (
    Address,
    AddressSet,
    AddressList,
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


@strawberry_django.filter(Address, lookups=True)
class NetBoxSecurityAddressFilter(
    ContactFilterMixin, TenancyFilterMixin, NetBoxModelFilterMixin
):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()


@strawberry_django.filter(AddressSet, lookups=True)
class NetBoxSecurityAddressSetFilter(
    ContactFilterMixin, TenancyFilterMixin, NetBoxModelFilterMixin
):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    addresses: (
        Annotated[
            "NetBoxSecurityAddressFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()


@strawberry_django.filter(AddressList, lookups=True)
class NetBoxSecurityAddressListFilter(NetBoxModelFilterMixin):
    name: FilterLookup[str] | None = strawberry_django.filter_field()


@strawberry_django.filter(SecurityZone, lookups=True)
class NetBoxSecuritySecurityZoneFilter(
    ContactFilterMixin, TenancyFilterMixin, NetBoxModelFilterMixin
):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()


@strawberry_django.filter(SecurityZonePolicy, lookups=True)
class NetBoxSecuritySecurityZonePolicyFilter(
    ContactFilterMixin, NetBoxModelFilterMixin
):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    index: FilterLookup[int] | None = strawberry_django.filter_field()
    source_zone: (
        Annotated[
            "NetBoxSecuritySecurityZoneFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    destination_zone: (
        Annotated[
            "NetBoxSecuritySecurityZoneFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    source_address: (
        Annotated[
            "NetBoxSecurityAddressListFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    destination_address: (
        Annotated[
            "NetBoxSecurityAddressListFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    policy_actions: (
        Annotated[
            "PolicyActionArrayLookup",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()


@strawberry_django.filter(NatPool, lookups=True)
class NetBoxSecurityNatPoolFilter(ContactFilterMixin, NetBoxModelFilterMixin):
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


@strawberry_django.filter(NatPoolMember, lookups=True)
class NetBoxSecurityNatPoolMemberFilter(NetBoxModelFilterMixin):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    pool: (
        Annotated[
            "NetBoxSecurityNatPoolFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    status: (
        Annotated["IPAddressStatusEnum", strawberry.lazy("ipam.graphql.enums")] | None
    ) = strawberry_django.filter_field()
    address: (
        Annotated["IPAddressFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    prefix: (
        Annotated["PrefixFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    address_range: (
        Annotated["IPRangeFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()


@strawberry_django.filter(NatRuleSet, lookups=True)
class NetBoxSecurityNatRuleSetFilter(ContactFilterMixin, NetBoxModelFilterMixin):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    nat_type: (
        Annotated[
            "NetBoxSecurityNatTypeEnum",
            strawberry.lazy("netbox_security.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()
    source_zones: (
        Annotated[
            "NetBoxSecuritySecurityZoneFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    destination_zones: (
        Annotated[
            "NetBoxSecuritySecurityZoneFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    direction: (
        Annotated[
            "NetBoxSecurityRuleDirectionEnum",
            strawberry.lazy("netbox_security.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()


@strawberry_django.filter(NatRule, lookups=True)
class NetBoxSecurityNatRuleFilter(ContactFilterMixin, NetBoxModelFilterMixin):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    rule_set: (
        Annotated[
            "NetBoxSecurityNatRuleSetFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    pool: (
        Annotated[
            "NetBoxSecurityNatPoolFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    source_pool: (
        Annotated[
            "NetBoxSecurityNatPoolFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    destination_pool: (
        Annotated[
            "NetBoxSecurityNatPoolFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
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


@strawberry_django.filter(Policer, lookups=True)
class NetBoxSecurityPolicerFilter(
    ContactFilterMixin, TenancyFilterMixin, NetBoxModelFilterMixin
):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    logical_interface_policer: FilterLookup[bool] | None = (
        strawberry_django.filter_field()
    )
    physical_interface_policer: FilterLookup[bool] | None = (
        strawberry_django.filter_field()
    )
    bandwidth_limit: FilterLookup[int] | None = strawberry_django.filter_field()
    bandwidth_percent: FilterLookup[int] | None = strawberry_django.filter_field()
    burst_size_limit: FilterLookup[int] | None = strawberry_django.filter_field()
    discard: FilterLookup[bool] | None = strawberry_django.filter_field()
    out_of_profile: FilterLookup[bool] | None = strawberry_django.filter_field()
    loss_priority: (
        Annotated[
            "NetBoxSecurityLossPriorityEnum",
            strawberry.lazy("netbox_security.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()
    forwarding_class: (
        Annotated[
            "NetBoxSecurityForwardingClassEnum",
            strawberry.lazy("netbox_security.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()


@strawberry_django.filter(FirewallFilter, lookups=True)
class NetBoxSecurityFirewallFilterFilter(
    ContactFilterMixin, TenancyFilterMixin, NetBoxModelFilterMixin
):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    family: (
        Annotated[
            "NetBoxSecurityFamilyEnum", strawberry.lazy("netbox_security.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()


@strawberry_django.filter(FirewallFilterRule, lookups=True)
class NetBoxSecurityFirewallFilterRuleFilter(
    ContactFilterMixin, NetBoxModelFilterMixin
):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    firewall_filter: (
        Annotated[
            "NetBoxSecurityFirewallFilterFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    index: FilterLookup[int] | None = strawberry_django.filter_field()
