from utilities.choices import ChoiceSet


class FamilyChoices(ChoiceSet):

    INET = 'inet'
    INET6 = 'inet6'
    ANY = 'any'
    MPLS = 'mpls'
    CCC = 'ccc'

    CHOICES = [
        (INET, 'INET', 'green'),
        (INET6, 'INET6', 'red'),
        (ANY, 'ANY', 'blue'),
        (MPLS, 'MPLS', 'cyan'),
        (CCC, 'CCC', 'orange'),
    ]


class FirewallRuleSettingChoices(ChoiceSet):
    ADDRESS = 'address'
    DESTINATION_ADDRESS = 'destination-address'
    DESTINATION_PORT = 'destination-port'
    DESTINATION_PREFIX_LIST = 'destination-prefix-list'
    PORT = 'port'
    INTERFACE = 'interface'
    PREFIX_LIST = 'prefix-list'
    PROTOCOL = 'protocol'
    SOURCE_ADDRESS = 'source-address'
    SOURCE_PORT = 'source-port'
    SOURCE_PREFIX_LIST = 'source-prefix-list'
    TCP_ESTABLISHED = 'tcp-established'

    CHOICES = [
        (ADDRESS, 'Address'),
        (DESTINATION_ADDRESS, 'Destination Address'),
        (DESTINATION_PORT, 'Destination Port'),
        (DESTINATION_PREFIX_LIST, 'Destination Prefix List'),
        (INTERFACE, 'Interface'),
        (PREFIX_LIST, 'Prefix List'),
        (SOURCE_ADDRESS, 'Source Address'),
        (SOURCE_PORT, 'Source Port'),
        (SOURCE_PREFIX_LIST, 'Source Prefix List'),
        (TCP_ESTABLISHED, 'TCP Established'),
    ]

    FIELD_TYPES = {
        ADDRESS: 'string',
        DESTINATION_ADDRESS: 'string',
        DESTINATION_PORT: 'string',
        DESTINATION_PREFIX_LIST: 'string',
        PORT: 'integer',
        INTERFACE: 'string',
        PREFIX_LIST: 'string',
        PROTOCOL: 'string',
        SOURCE_ADDRESS: 'string',
        SOURCE_PORT: 'integer',
        SOURCE_PREFIX_LIST: 'string',
        TCP_ESTABLISHED: 'boolean',
    }


class FirewallRuleFromSettingChoices(ChoiceSet):
    ACCEPT = 'accept'
    COUNT = 'count'
    DISCARD = 'discard'
    LOG = 'log'
    NEXT = 'nextt'
    POLICER = 'policier'
    REJECT = 'reject'
    SAMPLE = 'sample'
    SYSLOG = 'syslog'

    CHOICES = [
        (ACCEPT, 'Accept'),
        (COUNT, 'Count'),
        (DISCARD, 'Discard'),
        (LOG, 'Log'),
        (NEXT, 'Next'),
        (POLICER, 'Policer'),
        (REJECT, 'Reject'),
        (SAMPLE, 'Sample'),
        (SYSLOG, 'Syslog'),
    ]

    FIELD_TYPES = {
        ACCEPT: 'boolean',
        COUNT: 'boolean',
        DISCARD: 'boolean',
        LOG: 'boolean',
        NEXT: 'boolean',
        POLICER: 'boolean',
        REJECT: 'boolean',
        SAMPLE: 'boolean',
        SYSLOG: 'boolean',
    }


class FirewallRuleThenSettingChoices(ChoiceSet):
    ADDRESS = 'address'

    CHOICES = [
        (ADDRESS, 'Address'),
    ]

    FIELD_TYPES = {
        ADDRESS: 'ipaddr',
    }
