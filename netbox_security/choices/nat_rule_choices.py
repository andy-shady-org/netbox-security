from utilities.choices import ChoiceSet


__all__ = (
    "RuleDirectionChoices",
    "NatTypeChoices",
    "RuleStatusChoices",
    "CustomInterfaceChoices",
    "AddressTypeChoices",
)


class RuleDirectionChoices(ChoiceSet):
    DIRECTION_INBOUND = "inbound"
    DIRECTION_OUTBOUND = "outbound"

    CHOICES = (
        (DIRECTION_INBOUND, "Inbound", "blue"),
        (DIRECTION_OUTBOUND, "Outbound", "cyan"),
    )


class NatTypeChoices(ChoiceSet):
    TYPE_STATIC = "static"
    TYPE_DESTINATION = "destination"
    TYPE_SOURCE = "source"
    TYPE_IPV4 = "source"
    TYPE_NAT64 = "nat64"
    TYPE_NPTV6 = "nptv6"

    CHOICES = (
        (TYPE_STATIC, "Static", "blue"),
        (TYPE_DESTINATION, "Destination", "cyan"),
        (TYPE_SOURCE, "Source", "red"),
        (TYPE_IPV4, "IPv4", "orange"),
        (TYPE_NAT64, "NAT64", "brown"),
        (TYPE_NPTV6, "NPTv6", "green"),
    )


class RuleStatusChoices(ChoiceSet):

    STATUS_ACTIVE = "active"
    STATUS_RESERVED = "reserved"
    STATUS_DEPRECATED = "deprecated"

    CHOICES = (
        (STATUS_ACTIVE, "Active", "blue"),
        (STATUS_RESERVED, "Reserved", "cyan"),
        (STATUS_DEPRECATED, "Deprecated", "red"),
    )


class CustomInterfaceChoices(ChoiceSet):
    INTERFACE = "interface"
    NAT_OFF = "off"
    NONE = "None"

    CHOICES = (
        (INTERFACE, "Interface", "blue"),
        (NAT_OFF, "Off", "cyan"),
        (NONE, "None", "red"),
    )


class AddressTypeChoices(ChoiceSet):
    STATIC = "static"
    DYNAMIC = "dynamic"

    CHOICES = (
        (STATIC, "Static", "blue"),
        (DYNAMIC, "Dynamic", "cyan"),
    )
