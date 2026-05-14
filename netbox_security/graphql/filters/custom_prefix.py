import strawberry_django

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup


from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin, TenancyFilterMixin

from netbox_security.models import (
    CustomPrefix,
)

__all__ = ("NetBoxSecurityCustomPrefixFilter",)


@strawberry_django.filter(CustomPrefix, lookups=True)
class NetBoxSecurityCustomPrefixFilter(
    ContactFilterMixin, TenancyFilterMixin, PrimaryModelFilter
):
    prefix: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()
