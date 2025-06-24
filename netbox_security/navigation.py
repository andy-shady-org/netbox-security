from django.utils.translation import gettext_lazy as _
from django.conf import settings
from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu

plugin_settings = settings.PLUGINS_CONFIG.get("netbox_security", {})

address_menu_items = (
    PluginMenuItem(
        link="plugins:netbox_security:addressset_list",
        link_text=_("Address Sets"),
        permissions=["netbox_security.view_addressset"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_security:addressset_add",
                _("Add"),
                "mdi mdi-plus-thick",
                permissions=["netbox_security.add_addressset"],
            ),
            PluginMenuButton(
                "plugins:netbox_security:addressset_bulk_import",
                _("Import"),
                "mdi mdi-upload",
                permissions=["netbox_security.add_addressset"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_security:address_list",
        link_text=_("Addresses"),
        permissions=["netbox_security.view_address"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_security:address_add",
                _("Add"),
                "mdi mdi-plus-thick",
                permissions=["netbox_security.add_address"],
            ),
            PluginMenuButton(
                "plugins:netbox_security:address_bulk_import",
                _("Import"),
                "mdi mdi-upload",
                permissions=["netbox_security.add_address"],
            ),
        ),
    ),
)
application_menu_items = (
    PluginMenuItem(
        link="plugins:netbox_security:applicationitem_list",
        link_text=_("Application Items"),
        permissions=["netbox_security.view_applicationitem"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_security:applicationitem_add",
                _("Add"),
                "mdi mdi-plus-thick",
                permissions=["netbox_security.add_applicationitem"],
            ),
            PluginMenuButton(
                "plugins:netbox_security:applicationitem_bulk_import",
                _("Import"),
                "mdi mdi-upload",
                permissions=["netbox_security.add_applicationitem"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_security:application_list",
        link_text=_("Applications"),
        permissions=["netbox_security.view_application"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_security:application_add",
                _("Add"),
                "mdi mdi-plus-thick",
                permissions=["netbox_security.add_application"],
            ),
            PluginMenuButton(
                "plugins:netbox_security:application_bulk_import",
                _("Import"),
                "mdi mdi-upload",
                permissions=["netbox_security.add_application"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_security:applicationset_list",
        link_text=_("Application Sets"),
        permissions=["netbox_security.view_applicationset"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_security:applicationset_add",
                _("Add"),
                "mdi mdi-plus-thick",
                permissions=["netbox_security.add_applicationset"],
            ),
            PluginMenuButton(
                "plugins:netbox_security:applicationset_bulk_import",
                _("Import"),
                "mdi mdi-upload",
                permissions=["netbox_security.add_applicationset"],
            ),
        ),
    ),
)
security_menu_items = (
    PluginMenuItem(
        link="plugins:netbox_security:securityzone_list",
        link_text=_("Security Zones"),
        permissions=["netbox_security.view_securityzone"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_security:securityzone_add",
                _("Add"),
                "mdi mdi-plus-thick",
                permissions=["netbox_security.add_securityzone"],
            ),
            PluginMenuButton(
                "plugins:netbox_security:securityzone_bulk_import",
                _("Import"),
                "mdi mdi-upload",
                permissions=["netbox_security.add_securityzone"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_security:securityzonepolicy_list",
        link_text=_("Security Zone Policies"),
        permissions=["netbox_security.view_securityzonepolicy"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_security:securityzonepolicy_add",
                _("Add"),
                "mdi mdi-plus-thick",
                permissions=["netbox_security.add_securityzonepolicy"],
            ),
            PluginMenuButton(
                "plugins:netbox_security:securityzonepolicy_bulk_import",
                _("Import"),
                "mdi mdi-upload",
                permissions=["netbox_security.add_securityzonepolicy"],
            ),
        ),
    ),
)
pool_menu_items = (
    PluginMenuItem(
        link="plugins:netbox_security:natpool_list",
        link_text=_("NAT Pools"),
        permissions=["netbox_security.view_natpool"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_security:natpool_add",
                _("Add"),
                "mdi mdi-plus-thick",
                permissions=["netbox_security.add_natpool"],
            ),
            PluginMenuButton(
                "plugins:netbox_security:natpool_bulk_import",
                _("Import"),
                "mdi mdi-upload",
                permissions=["netbox_security.add_natpool"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_security:natpoolmember_list",
        link_text=_("Pool Members"),
        permissions=["netbox_security.view_natpoolmember"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_security:natpoolmember_add",
                _("Add"),
                "mdi mdi-plus-thick",
                permissions=["netbox_security.add_natpoolmember"],
            ),
            PluginMenuButton(
                "plugins:netbox_security:natpoolmember_bulk_import",
                _("Import"),
                "mdi mdi-upload",
                permissions=["netbox_security.add_natpoolmember"],
            ),
        ),
    ),
)
rule_menu_items = (
    PluginMenuItem(
        link="plugins:netbox_security:natruleset_list",
        link_text=_("NAT Rule Sets"),
        permissions=["netbox_security.view_natruleset"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_security:natruleset_add",
                _("Add"),
                "mdi mdi-plus-thick",
                permissions=["netbox_security.add_natruleset"],
            ),
            PluginMenuButton(
                "plugins:netbox_security:natruleset_bulk_import",
                _("Import"),
                "mdi mdi-upload",
                permissions=["netbox_security.add_natruleset"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_security:natrule_list",
        link_text="NAT Rules",
        permissions=["netbox_security.view_natrule"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_security:natrule_add",
                _("Add"),
                "mdi mdi-plus-thick",
                permissions=["netbox_security.add_natrule"],
            ),
            PluginMenuButton(
                "plugins:netbox_security:natrule_bulk_import",
                _("Import"),
                "mdi mdi-upload",
                permissions=["netbox_security.add_natrule"],
            ),
        ),
    ),
)

firewall_menu_items = (
    PluginMenuItem(
        link="plugins:netbox_security:firewallfilter_list",
        link_text=_("Firewall Filters"),
        permissions=["netbox_security.view_firewallfilter"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_security:firewallfilter_add",
                _("Add"),
                "mdi mdi-plus-thick",
                permissions=["netbox_security.add_firewallfilter"],
            ),
            PluginMenuButton(
                "plugins:netbox_security:firewallfilter_bulk_import",
                _("Import"),
                "mdi mdi-upload",
                permissions=["netbox_security.add_firewallfilter"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_security:firewallfilterrule_list",
        link_text="Firewall Filter Rules",
        permissions=["netbox_security.view_firewallfilterrule"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_security:firewallfilterrule_add",
                _("Add"),
                "mdi mdi-plus-thick",
                permissions=["netbox_security.add_firewallfilterrule"],
            ),
            PluginMenuButton(
                "plugins:netbox_security:firewallfilterrule_bulk_import",
                _("Import"),
                "mdi mdi-upload",
                permissions=["netbox_security.add_firewallfilterrule"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_security:policer_list",
        link_text="Firewall Policers",
        permissions=["netbox_security.view_policer"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_security:policer_add",
                _("Add"),
                "mdi mdi-plus-thick",
                permissions=["netbox_security.add_policer"],
            ),
            PluginMenuButton(
                "plugins:netbox_security:policer_bulk_import",
                _("Import"),
                "mdi mdi-upload",
                permissions=["netbox_security.add_policer"],
            ),
        ),
    ),
)


if plugin_settings.get("top_level_menu"):
    menu = PluginMenu(
        label=_("Security"),
        groups=(
            (_("Address Book"), address_menu_items),
            (_("Applications"), application_menu_items),
            (_("Security Zones"), security_menu_items),
            (_("NAT Pools"), pool_menu_items),
            (_("NAT Rules"), rule_menu_items),
            (_("Firewall Filters"), firewall_menu_items),
        ),
        icon_class="mdi mdi-security",
    )
else:
    menu_items = (
        address_menu_items
        + application_menu_items
        + security_menu_items
        + pool_menu_items
        + rule_menu_items
        + firewall_menu_items
    )
