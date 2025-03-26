from utilities.choices import ChoiceSet


class ActionChoices(ChoiceSet):

    PERMIT = 'permit'
    DENY = 'deny'
    LOG = 'log'
    COUNT = 'count'
    REJECT = 'reject'

    CHOICES = [
        (PERMIT, 'Permit', 'green'),
        (DENY, 'Deny', 'red'),
        (LOG, 'Log', 'blue'),
        (COUNT, 'Count', 'cyan'),
        (REJECT, 'Reject', 'red'),
    ]
