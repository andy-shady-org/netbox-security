from utilities.choices import ChoiceSet

__all__ = ("PoolTypeChoices",)


class PoolTypeChoices(ChoiceSet):
    ADDRESS = "address"
    HOST_ADDRESS_BASE = "host-address-base"

    CHOICES = (
        (ADDRESS, "address", "blue"),
        (HOST_ADDRESS_BASE, "host-address-base", "cyan"),
    )
