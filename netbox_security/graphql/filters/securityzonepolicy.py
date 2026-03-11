from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import ComparisonFilterLookup
from strawberry.scalars import ID

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin

from netbox_security.graphql.filter_lookups import (
    PolicyActionArrayLookup,
)


from netbox_security.models import (
    SecurityZonePolicy,
)

from .securityzone import NetBoxSecuritySecurityZoneFilter
from .address_list import NetBoxSecurityAddressListFilter
from .application import NetBoxSecurityApplicationFilter
from .application_set import NetBoxSecurityApplicationSetFilter

__all__ = ("NetBoxSecuritySecurityZonePolicyFilter",)


@strawberry_django.filter(SecurityZonePolicy, lookups=True)
class NetBoxSecuritySecurityZonePolicyFilter(ContactFilterMixin, PrimaryModelFilter):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    identifier: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()
    index: ComparisonFilterLookup[int] | None = strawberry_django.filter_field()
    source_zone: (
        Annotated[
            "NetBoxSecuritySecurityZoneFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    source_zone_id: ID | None = strawberry_django.filter_field()
    destination_zone: (
        Annotated[
            "NetBoxSecuritySecurityZoneFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    destination_zone_id: ID | None = strawberry_django.filter_field()
    source_address: (
        Annotated[
            "NetBoxSecurityAddressListFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    source_address_id: ID | None = strawberry_django.filter_field()
    destination_address: (
        Annotated[
            "NetBoxSecurityAddressListFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    destination_address_id: ID | None = strawberry_django.filter_field()
    applications: (
        Annotated[
            "NetBoxSecurityApplicationFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    application_sets: (
        Annotated[
            "NetBoxSecurityApplicationSetFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    policy_actions: (
        Annotated[
            "PolicyActionArrayLookup",
            strawberry.lazy("netbox_security.graphql.filter_lookups"),
        ]
        | None
    ) = strawberry_django.filter_field()
