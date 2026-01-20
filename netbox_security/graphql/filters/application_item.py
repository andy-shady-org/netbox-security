from typing import Annotated, List
import strawberry
import strawberry_django
from strawberry_django import FilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin

from netbox_security.graphql.filter_lookups import (
    ProtocolArrayLookup,
)

from netbox_security.models import (
    ApplicationItem,
)

__all__ = ("NetBoxSecurityApplicationItemFilter",)


@strawberry_django.filter(ApplicationItem, lookups=True)
class NetBoxSecurityApplicationItemFilter(ContactFilterMixin, PrimaryModelFilter):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    index: FilterLookup[int] | None = strawberry_django.filter_field()
    protocol: (
        Annotated[
            "ProtocolArrayLookup",
            strawberry.lazy("netbox_security.graphql.filter_lookups"),
        ]
        | None
    ) = strawberry_django.filter_field()
    destination_ports: List[FilterLookup[int]] | None = strawberry_django.filter_field()
    source_ports: List[FilterLookup[int]] | None = strawberry_django.filter_field()
