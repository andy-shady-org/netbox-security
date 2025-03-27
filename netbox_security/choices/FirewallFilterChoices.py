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

    CHOICES = [
        (ADDRESS, 'Address'),
    ]

    FIELD_TYPES = {
        ADDRESS: 'ipaddr',
    }


class FirewallRuleFromSettingChoices(ChoiceSet):
    ADDRESS = 'address'

    CHOICES = [
        (ADDRESS, 'Address'),
    ]

    FIELD_TYPES = {
        ADDRESS: 'ipaddr',
    }


class FirewallRuleThenSettingChoices(ChoiceSet):
    ADDRESS = 'address'

    CHOICES = [
        (ADDRESS, 'Address'),
    ]

    FIELD_TYPES = {
        ADDRESS: 'ipaddr',
    }
