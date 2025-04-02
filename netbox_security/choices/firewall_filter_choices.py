from utilities.choices import ChoiceSet


__all__ = (
    "FamilyChoices",
    "FirewallRuleFromSettingChoices",
    "FirewallRuleThenSettingChoices",
)


class FamilyChoices(ChoiceSet):

    INET = "inet"
    INET6 = "inet6"
    ANY = "any"
    MPLS = "mpls"
    CCC = "ccc"

    CHOICES = [
        (INET, "INET", "green"),
        (INET6, "INET6", "red"),
        (ANY, "ANY", "blue"),
        (MPLS, "MPLS", "cyan"),
        (CCC, "CCC", "orange"),
    ]


class FirewallRuleFromSettingChoices(ChoiceSet):
    ADDRESS = "address"
    DESTINATION_ADDRESS = "destination_address"
    DESTINATION_PORT = "destination_port"
    DESTINATION_PREFIX_LIST = "destination_prefix_ist"
    PORT = "port"
    INTERFACE = "interface"
    PREFIX_LIST = "prefix_list"
    PROTOCOL = "protocol"
    SOURCE_ADDRESS = "source_address"
    SOURCE_PORT = "source_port"
    SOURCE_PREFIX_LIST = "source_prefix_list"
    TCP_ESTABLISHED = "tcp_established"

    CHOICES = [
        (ADDRESS, "Address"),
        (DESTINATION_ADDRESS, "Destination Address"),
        (DESTINATION_PORT, "Destination Port"),
        (DESTINATION_PREFIX_LIST, "Destination Prefix List"),
        (PORT, "Port"),
        (INTERFACE, "Interface"),
        (PREFIX_LIST, "Prefix List"),
        (PROTOCOL, "Protocol"),
        (SOURCE_ADDRESS, "Source Address"),
        (SOURCE_PORT, "Source Port"),
        (SOURCE_PREFIX_LIST, "Source Prefix List"),
        (TCP_ESTABLISHED, "TCP Established"),
    ]

    FIELD_TYPES = {
        ADDRESS: "string",
        DESTINATION_ADDRESS: "string",
        DESTINATION_PORT: "integer",
        DESTINATION_PREFIX_LIST: "string",
        PORT: "integer",
        INTERFACE: "string",
        PREFIX_LIST: "string",
        PROTOCOL: "string",
        SOURCE_ADDRESS: "string",
        SOURCE_PORT: "integer",
        SOURCE_PREFIX_LIST: "string",
        TCP_ESTABLISHED: "boolean",
    }


class FirewallRuleThenSettingChoices(ChoiceSet):
    ACCEPT = "accept"
    COUNT = "count"
    DISCARD = "discard"
    LOG = "log"
    NEXT = "next"
    POLICER = "policier"
    REJECT = "reject"
    SAMPLE = "sample"
    SYSLOG = "syslog"

    CHOICES = [
        (ACCEPT, "Accept"),
        (COUNT, "Count"),
        (DISCARD, "Discard"),
        (LOG, "Log"),
        (NEXT, "Next"),
        (POLICER, "Policer"),
        (REJECT, "Reject"),
        (SAMPLE, "Sample"),
        (SYSLOG, "Syslog"),
    ]

    FIELD_TYPES = {
        ACCEPT: "boolean",
        COUNT: "boolean",
        DISCARD: "boolean",
        LOG: "boolean",
        NEXT: "boolean",
        POLICER: "boolean",
        REJECT: "boolean",
        SAMPLE: "boolean",
        SYSLOG: "boolean",
    }
