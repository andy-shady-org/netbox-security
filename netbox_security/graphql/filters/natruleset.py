from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin

from netbox_security.graphql.enums import (
    NetBoxSecurityRuleDirectionEnum,
    NetBoxSecurityNatTypeEnum,
)

from netbox_security.models import (
    NatRuleSet,
)

from .securityzone import NetBoxSecuritySecurityZoneFilter

__all__ = ("NetBoxSecurityNatRuleSetFilter",)


@strawberry_django.filter(NatRuleSet, lookups=True)
class NetBoxSecurityNatRuleSetFilter(ContactFilterMixin, PrimaryModelFilter):
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
