from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin, TenancyFilterMixin

from netbox_security.graphql.enums import (
    NetBoxSecurityLossPriorityEnum,
    NetBoxSecurityForwardingClassEnum,
)

from netbox_security.models import (
    Policer,
)

__all__ = ("NetBoxSecurityPolicerFilter",)


@strawberry_django.filter(Policer, lookups=True)
class NetBoxSecurityPolicerFilter(
    ContactFilterMixin, TenancyFilterMixin, PrimaryModelFilter
):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()
    logical_interface_policer: FilterLookup[bool] | None = (
        strawberry_django.filter_field()
    )
    physical_interface_policer: FilterLookup[bool] | None = (
        strawberry_django.filter_field()
    )
    bandwidth_limit: (
        Annotated["IntegerLookup", strawberry.lazy("netbox.graphql.filter_lookups")]
        | None
    ) = strawberry_django.filter_field()
    bandwidth_percent: (
        Annotated["IntegerLookup", strawberry.lazy("netbox.graphql.filter_lookups")]
        | None
    ) = strawberry_django.filter_field()
    burst_size_limit: (
        Annotated["IntegerLookup", strawberry.lazy("netbox.graphql.filter_lookups")]
        | None
    ) = strawberry_django.filter_field()
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
