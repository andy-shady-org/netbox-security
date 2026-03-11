from typing import Annotated
import strawberry
import strawberry_django
from strawberry.scalars import ID

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filter_lookups import IntegerLookup
from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin


from netbox_security.models import (
    FirewallFilterRule,
)

from .firewallfilter import NetBoxSecurityFirewallFilterFilter

__all__ = ("NetBoxSecurityFirewallFilterRuleFilter",)


@strawberry_django.filter(FirewallFilterRule, lookups=True)
class NetBoxSecurityFirewallFilterRuleFilter(ContactFilterMixin, PrimaryModelFilter):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()
    firewall_filter: (
        Annotated[
            "NetBoxSecurityFirewallFilterFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    firewall_filter_id: ID | None = strawberry_django.filter_field()
    index: (
        Annotated["IntegerLookup", strawberry.lazy("netbox.graphql.filter_lookups")]
        | None
    ) = strawberry_django.filter_field()
