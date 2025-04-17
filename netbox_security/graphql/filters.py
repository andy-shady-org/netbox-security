import strawberry_django

from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin

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
)

from netbox_security.filtersets import (
    AddressFilterSet,
    AddressSetFilterSet,
    AddressListFilterSet,
    SecurityZoneFilterSet,
    SecurityZonePolicyFilterSet,
    NatPoolFilterSet,
    NatPoolMemberFilterSet,
    NatRuleSetFilterSet,
    NatRuleFilterSet,
    FirewallFilterFilterSet,
    FirewallFilterRuleFilterSet,
)


@strawberry_django.filter(Address, lookups=True)
@autotype_decorator(AddressFilterSet)
class NetBoxSecurityAddressFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(AddressSet, lookups=True)
@autotype_decorator(AddressSetFilterSet)
class NetBoxSecurityAddressSetFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(AddressList, lookups=True)
@autotype_decorator(AddressListFilterSet)
class NetBoxSecurityAddressListFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(SecurityZone, lookups=True)
@autotype_decorator(SecurityZoneFilterSet)
class NetBoxSecuritySecurityZoneFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(SecurityZonePolicy, lookups=True)
@autotype_decorator(SecurityZonePolicyFilterSet)
class NetBoxSecuritySecurityZonePolicyFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(NatPool, lookups=True)
@autotype_decorator(NatPoolFilterSet)
class NetBoxSecurityNatPoolFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(NatPoolMember, lookups=True)
@autotype_decorator(NatPoolMemberFilterSet)
class NetBoxSecurityNatPoolMemberFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(NatRuleSet, lookups=True)
@autotype_decorator(NatRuleSetFilterSet)
class NetBoxSecurityNatRuleSetFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(NatRule, lookups=True)
@autotype_decorator(NatRuleFilterSet)
class NetBoxSecurityNatRuleFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(FirewallFilter, lookups=True)
@autotype_decorator(FirewallFilterFilterSet)
class NetBoxSecurityFirewallFilterFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(FirewallFilterRule, lookups=True)
@autotype_decorator(FirewallFilterRuleFilterSet)
class NetBoxSecurityFirewallFilterRuleFilter(BaseFilterMixin):
    pass
