from typing import List

import strawberry
import strawberry_django

from .types import (
    NetBoxSecurityAddressType,
    NetBoxSecurityAddressSetType,
    NetBoxSecurityAddressListType,
    NetBoxSecuritySecurityZoneType,
    NetBoxSecuritySecurityZonePolicyType,
    NetBoxSecurityNatPoolType,
    NetBoxSecurityNatPoolMemberType,
    NetBoxSecurityNatRuleSetType,
    NetBoxSecurityNatRuleType,
)


@strawberry.type(name="Query")
class NetBoxSecurityAddressQuery:
    netbox_security_addresslist: NetBoxSecurityAddressType = strawberry_django.field()
    netbox_security_addresslist_list: List[NetBoxSecurityAddressType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecurityAddressSetQuery:
    netbox_security_addresssetlist: NetBoxSecurityAddressSetType = strawberry_django.field()
    netbox_security_addresssetlist_list: List[NetBoxSecurityAddressSetType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecurityAddressListQuery:
    netbox_security_addresslistlist: NetBoxSecurityAddressListType = strawberry_django.field()
    netbox_security_addresslistlist_list: List[NetBoxSecurityAddressListType] = (
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
class NetBoxSecurityNatRuleSetQuery:
    netbox_security_natrule: NetBoxSecurityNatRuleSetType = strawberry_django.field()
    netbox_security_natrule_list: List[NetBoxSecurityNatRuleSetType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxSecurityNatRuleQuery:
    netbox_security_natruleset: NetBoxSecurityNatRuleType = strawberry_django.field()
    netbox_security_natruleset_list: List[NetBoxSecurityNatRuleType] = (
        strawberry_django.field()
    )
