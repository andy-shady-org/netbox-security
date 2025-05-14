from utilities.choices import ChoiceSet


__all__ = ("ForwardingClassChoices", "LossPriorityChoices")


class ForwardingClassChoices(ChoiceSet):
    ASSURED_FORWARDING = "assured-forwarding"
    BEST_EFFORT = "best-effort"
    EXPEDITED_FORWARDING = "expedited-forwarding"
    NETWORK_CONTROL = "network-control"

    CHOICES = [
        (ASSURED_FORWARDING, "Assured Forwarding", "green"),
        (BEST_EFFORT, "Best Effort", "red"),
        (EXPEDITED_FORWARDING, "Expedited Forwarding", "orange"),
        (NETWORK_CONTROL, "Network Control", "blue"),
    ]


class LossPriorityChoices(ChoiceSet):
    HIGH = "high"
    LOW = "low"
    MEDIUM_HIGH = "medium-high"
    MEDIUM_LOW = "medium-low"

    CHOICES = [
        (HIGH, "High", "green"),
        (LOW, "Low", "red"),
        (MEDIUM_HIGH, "Medium High", "orange"),
        (MEDIUM_LOW, "Medium High", "blue"),
    ]
