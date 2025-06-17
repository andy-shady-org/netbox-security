import re
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate_fqdn(name):
    allowed = re.compile(r"(?!-)\*?_?[A-Z_\d-]{0,63}(?<!-)$", re.IGNORECASE)
    if len(name.split(".")) < 2:
        raise ValidationError(
            _("{name} is not a valid fully qualified DNS host name").format(name=name)
        )
    if not all(allowed.match(x) for x in name.split(".")):
        raise ValidationError(
            _("{name} is not a valid fully qualified DNS host name").format(name=name)
        )
