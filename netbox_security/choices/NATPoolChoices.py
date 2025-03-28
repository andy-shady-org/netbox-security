from utilities.choices import ChoiceSet
from django.utils.translation import gettext_lazy as _


class PoolTypeChoices(ChoiceSet):
    ADDRESS = "address"
    HOST_ADDRESS_BASE = "host-address-base"

    CHOICES = (
        (ADDRESS, "address", "blue"),
        (HOST_ADDRESS_BASE, "host-address-base", "cyan"),
    )
