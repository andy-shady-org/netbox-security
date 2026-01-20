from typing import Annotated, List
import strawberry
import strawberry_django
from strawberry_django import FilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin, TenancyFilterMixin

from netbox_security.graphql.filter_lookups import (
    ProtocolArrayLookup,
)

from netbox_security.models import (
    Application,
)

from .application_item import NetBoxSecurityApplicationItemFilter

__all__ = ("NetBoxSecurityApplicationFilter",)


@strawberry_django.filter(Application, lookups=True)
class NetBoxSecurityApplicationFilter(
    ContactFilterMixin, TenancyFilterMixin, PrimaryModelFilter
):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    identifier: FilterLookup[str] | None = strawberry_django.filter_field()
    application_items: (
        Annotated[
            "NetBoxSecurityApplicationItemFilter",
            strawberry.lazy("netbox_security.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    protocol: (
        Annotated[
            "ProtocolArrayLookup",
            strawberry.lazy("netbox_security.graphql.filter_lookups"),
        ]
        | None
    ) = strawberry_django.filter_field()
    destination_ports: List[FilterLookup[int]] | None = strawberry_django.filter_field()
    source_ports: List[FilterLookup[int]] | None = strawberry_django.filter_field()
