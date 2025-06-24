from typing import List

import strawberry
import strawberry_django

from .types import (
    NetBoxSecurityAddressType,
    NetBoxSecurityAddressSetType,
    NetBoxSecurityAddressListType,
    NetBoxSecurityApplicationItemType,
    NetBoxSecurityApplicationType,
    NetBoxSecurityApplicationSetType,
    NetBoxSecuritySecurityZoneType,
    NetBoxSecuritySecurityZonePolicyType,
    NetBoxSecurityNatPoolType,
    NetBoxSecurityNatPoolMemberType,
    NetBoxSecurityNatRuleSetType,
    NetBoxSecurityNatRuleType,
    NetBoxSecurityPolicerType,
    NetBoxSecurityFirewallFilterType,
    NetBoxSecurityFirewallFilterRuleType,
)


@strawberry.type(name="Query")
class NetBoxSecurityAddressQuery:
    netbox_security_address: NetBoxSecurityAddressType = strawberry_django.field()
    netbox_security_address_list: List[NetBoxSecurityAddressType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecurityAddressSetQuery:
    netbox_security_addressset: NetBoxSecurityAddressSetType = strawberry_django.field()
    netbox_security_addressset_list: List[NetBoxSecurityAddressSetType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecurityAddressListQuery:
    netbox_security_addresslist: NetBoxSecurityAddressListType = (
        strawberry_django.field()
    )
    netbox_security_addresslist_list: List[NetBoxSecurityAddressListType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecurityApplicationItemQuery:
    netbox_security_applicationitem: NetBoxSecurityApplicationItemType = (
        strawberry_django.field()
    )
    netbox_security_applicationitem_list: List[NetBoxSecurityApplicationItemType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecurityApplicationQuery:
    netbox_security_application: NetBoxSecurityApplicationType = (
        strawberry_django.field()
    )
    netbox_security_application_list: List[NetBoxSecurityApplicationType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecurityApplicationSetQuery:
    netbox_security_applicationset: NetBoxSecurityApplicationSetType = (
        strawberry_django.field()
    )
    netbox_security_applicationset_list: List[NetBoxSecurityApplicationSetType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecuritySecurityZoneQuery:
    netbox_security_securityzone: NetBoxSecuritySecurityZoneType = (
        strawberry_django.field()
    )
    netbox_security_securityzone_list: List[NetBoxSecuritySecurityZoneType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecuritySecurityZonePolicyQuery:
    netbox_security_securityzonepolicy: NetBoxSecuritySecurityZonePolicyType = (
        strawberry_django.field()
    )
    netbox_security_securityzonepolicy_list: List[
        NetBoxSecuritySecurityZonePolicyType
    ] = strawberry_django.field()


@strawberry.type(name="Query")
class NetBoxSecurityNatPoolQuery:
    netbox_security_natpool: NetBoxSecurityNatPoolType = strawberry_django.field()
    netbox_security_natpool_list: List[NetBoxSecurityNatPoolType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecurityNatPoolMemberQuery:
    netbox_security_natpoolmember: NetBoxSecurityNatPoolMemberType = (
        strawberry_django.field()
    )
    netbox_security_natpoolmember_list: List[NetBoxSecurityNatPoolMemberType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecurityNatRuleQuery:
    netbox_security_natrule: NetBoxSecurityNatRuleType = strawberry_django.field()
    netbox_security_natrule_list: List[NetBoxSecurityNatRuleType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecurityNatRuleSetQuery:
    netbox_security_natruleset: NetBoxSecurityNatRuleSetType = strawberry_django.field()
    netbox_security_natruleset_list: List[NetBoxSecurityNatRuleSetType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecurityPolicerQuery:
    netbox_security_policer: NetBoxSecurityPolicerType = strawberry_django.field()
    netbox_security_policer_list: List[NetBoxSecurityPolicerType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecurityFirewallFilterQuery:
    netbox_security_firewallfilter: NetBoxSecurityFirewallFilterType = (
        strawberry_django.field()
    )
    netbox_security_firewallfilter_list: List[NetBoxSecurityFirewallFilterType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecurityFirewallFilterRuleQuery:
    netbox_security_firewallfilterrule: NetBoxSecurityFirewallFilterRuleType = (
        strawberry_django.field()
    )
    netbox_security_firewallfilterrule_list: List[
        NetBoxSecurityFirewallFilterRuleType
    ] = strawberry_django.field()
