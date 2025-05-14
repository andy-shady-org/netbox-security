from django.utils.translation import gettext_lazy as _
from netbox.plugins import PluginConfig
from .version import __version__


class SecurityConfig(PluginConfig):
    name = "netbox_security"
    verbose_name = _("Netbox Security")
    description = _("A Netbox plugin for tracking Security and NAT related objects")
    version = __version__
    author = "Andy Wilson"
    author_email = "andy@shady.org"
    base_url = "netbox-security"
    required_settings = []
    min_version = "4.3.0"
    default_settings = {
        "top_level_menu": True,
        "virtual_ext_page": "left",
        "device_ext_page": "left",
        "interface_ext_page": "left",
        "address_ext_page": "right",
    }


config = SecurityConfig  # noqa
