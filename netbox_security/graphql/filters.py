import strawberry_django

from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin

from netbox_security.models import (
    AddressList,
    SecurityZone,
    NatPool,
    NatPoolMember,
    NatRuleSet,
    NatRule
)

from netbox_security.filtersets import (
    AddressListFilterSet,
    SecurityZoneFilterSet,
    NatPoolFilterSet,
    NatPoolMemberFilterSet,
    NatRuleSetFilterSet,
    NatRuleFilterSet,
)


@strawberry_django.filter(AddressList, lookups=True)
@autotype_decorator(AddressListFilterSet)
class NetBoxSecurityAddressListFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(SecurityZone, lookups=True)
@autotype_decorator(SecurityZoneFilterSet)
class NetBoxSecuritySecurityZoneFilter(BaseFilterMixin):
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
