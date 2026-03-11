from typing import Annotated
import strawberry
import strawberry_django

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin, TenancyFilterMixin

from netbox_security.models import (
    ApplicationSet,
)

from .application import NetBoxSecurityApplicationFilter

__all__ = ("NetBoxSecurityApplicationSetFilter",)


@strawberry_django.filter(ApplicationSet, lookups=True)
class NetBoxSecurityApplicationSetFilter(
    ContactFilterMixin, TenancyFilterMixin, PrimaryModelFilter
):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    identifier: StrFilterLookup[str] | None = strawberry_django.filter_field()
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
