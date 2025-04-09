from utilities.choices import ChoiceSet

__all__ = ("ActionChoices",)


class ActionChoices(ChoiceSet):

    PERMIT = "permit"
    DENY = "deny"
    LOG = "log"
    COUNT = "count"
    REJECT = "reject"

    CHOICES = [
        (PERMIT, "Permit", "green"),
        (DENY, "Deny", "red"),
        (LOG, "Log", "orange"),
        (COUNT, "Count", "orange"),
        (REJECT, "Reject", "red"),
    ]
