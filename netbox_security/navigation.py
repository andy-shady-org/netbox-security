from django.utils.translation import gettext_lazy as _
from django.conf import settings
from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_security', {})


security_menu_items = (
    PluginMenuItem(
        link='plugins:netbox_security:address_list',
        link_text='Addresses',
        permissions=['netbox_security.view_address'],
        buttons=(
            PluginMenuButton(
                'plugins:netbox_security:address_add',
                _("Add"),
                'mdi mdi-plus-thick',
                permissions=['netbox_security.add_address'],
            ),
            PluginMenuButton(
                'plugins:netbox_security:address_import',
                _("Import"),
                'mdi mdi-upload',
                permissions=['netbox_security.add_address'],
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_security:securityzone_list',
        link_text='Security Zones',
        permissions=['netbox_security.view_securityzone'],
        buttons=(
            PluginMenuButton(
                'plugins:netbox_security:securityzone_add',
                _("Add"),
                'mdi mdi-plus-thick',
                permissions=['netbox_security.add_securityzone'],
            ),
            PluginMenuButton(
                'plugins:netbox_security:securityzone_import',
                _("Import"),
                'mdi mdi-upload',
                permissions=['netbox_security.add_securityzone'],
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_security:securityzonepolicy_list',
        link_text='Security Zone Policies',
        permissions=['netbox_security.view_securityzonepolicy'],
        buttons=(
            PluginMenuButton(
                'plugins:netbox_security:securityzonepolicy_add',
                _("Add"),
                'mdi mdi-plus-thick',
                permissions=['netbox_security.add_securityzonepolicy'],
            ),
            PluginMenuButton(
                'plugins:netbox_security:securityzonepolicy_import',
                _("Import"),
                'mdi mdi-upload',
                permissions=['netbox_security.add_securityzonepolicy'],
            ),
        ),
    ),
)
pool_menu_items = (
    PluginMenuItem(
        link='plugins:netbox_security:natpool_list',
        link_text='NAT Pools',
        permissions=['netbox_security.view_natpool'],
        buttons=(
            PluginMenuButton(
                'plugins:netbox_security:natpool_add',
                _("Add"),
                'mdi mdi-plus-thick',
                permissions=['netbox_security.add_natpool'],
            ),
            PluginMenuButton(
                'plugins:netbox_security:natpool_import',
                _("Import"),
                'mdi mdi-upload',
                permissions=['netbox_security.add_natpool'],
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_security:natpoolmember_list',
        link_text='Pool Members',
        permissions=['netbox_security.view_natpoolmember'],
        buttons=(
            PluginMenuButton(
                'plugins:netbox_security:natpoolmember_add',
                _("Add"),
                'mdi mdi-plus-thick',
                permissions=['netbox_security.add_natpoolmember'],
            ),
            PluginMenuButton(
                'plugins:netbox_security:natpoolmember_import',
                _("Import"),
                'mdi mdi-upload',
                permissions=['netbox_security.add_natpoolmember'],
            ),
        ),
    ),
)
rule_menu_items = (
    PluginMenuItem(
        link='plugins:netbox_security:natruleset_list',
        link_text='NAT Rule Sets',
        permissions=['netbox_security.view_natruleset'],
        buttons=(
            PluginMenuButton(
                'plugins:netbox_security:natruleset_add',
                _("Add"),
                'mdi mdi-plus-thick',
                permissions=['netbox_security.add_natruleset'],
            ),
            PluginMenuButton(
                'plugins:netbox_security:natruleset_import',
                _("Import"),
                'mdi mdi-upload',
                permissions=['netbox_security.add_natruleset'],
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_security:natrule_list',
        link_text='NAT Rules',
        permissions=['netbox_security.view_natrule'],
        buttons=(
            PluginMenuButton(
                'plugins:netbox_security:natrule_add',
                _("Add"),
                'mdi mdi-plus-thick',
                permissions=['netbox_security.add_natrule'],
            ),
            PluginMenuButton(
                'plugins:netbox_security:natrule_import',
                _("Import"),
                'mdi mdi-upload',
                permissions=['netbox_security.add_natrule'],
            ),
        ),
    ),
)

firewall_menu_items = (
    PluginMenuItem(
        link='plugins:netbox_security:firewallfilter_list',
        link_text='Firewall Filters',
        permissions=['netbox_security.view_firewallfilter'],
        buttons=(
            PluginMenuButton(
                'plugins:netbox_security:firewallfilter_add',
                _("Add"),
                'mdi mdi-plus-thick',
                permissions=['netbox_security.add_firewallfilter'],
            ),
            PluginMenuButton(
                'plugins:netbox_security:firewallfilter_import',
                _("Import"),
                'mdi mdi-upload',
                permissions=['netbox_security.add_firewallfilter'],
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_security:firewallfilterrule_list',
        link_text='Firewall Filter Rules',
        permissions=['netbox_security.view_firewallfilterrule'],
        buttons=(
            PluginMenuButton(
                'plugins:netbox_security:firewallfilterrule_add',
                _("Add"),
                'mdi mdi-plus-thick',
                permissions=['netbox_security.add_firewallfilterrule'],
            ),
        ),
    ),
)

if plugin_settings.get('top_level_menu'):
    menu = PluginMenu(
        label="Security",
        groups=(
            ("Security Zones", security_menu_items),
            ("NAT Pools", pool_menu_items),
            ("NAT Rules", rule_menu_items),
            ("Firewall Filters", firewall_menu_items),
        ),
        icon_class="mdi mdi-security",
    )
else:
    menu_items = (security_menu_items + pool_menu_items + rule_menu_items + firewall_menu_items)
