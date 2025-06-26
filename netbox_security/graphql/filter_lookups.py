import strawberry

from netbox.graphql.filter_lookups import ArrayLookup

from netbox_security.graphql.enums import (
    NetBoxSecurityActionEnum,
    NetBoxSecurityProtocolEnum,
)


@strawberry.input(
    one_of=True,
    description="Lookup for Array fields. Only one of the lookup fields can be set.",
)
class PolicyActionArrayLookup(ArrayLookup[NetBoxSecurityActionEnum]):
    pass


@strawberry.input(
    one_of=True,
    description="Lookup fields. Multiple fields can be set.",
)
class ProtocolArrayLookup(ArrayLookup[NetBoxSecurityProtocolEnum]):
    pass
