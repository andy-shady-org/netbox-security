from netbox.plugins import PluginTemplateExtension

from netbox_security.models import (
    NatPoolAssignment,
    NatRuleSetAssignment,
    NatRuleAssignment,
    ApplicationAssignment,
    ApplicationSetAssignment,
    SecurityZoneAssignment,
    AddressAssignment,
    AddressSetAssignment,
    AddressList,
    FirewallFilterAssignment,
    PolicerAssignment,
)
from netbox_security.tables import (
    NatPoolDeviceAssignmentTable,
    NatPoolVirtualDeviceContextAssignmentTable,
    NatPoolVirtualMachineAssignmentTable,
    NatRuleSetDeviceAssignmentTable,
    NatRuleSetVirtualDeviceContextAssignmentTable,
    NatRuleSetVirtualMachineAssignmentTable,
    NatRuleAssignmentTable,
    ApplicationDeviceAssignmentTable,
    ApplicationVirtualDeviceContextAssignmentTable,
    ApplicationSetDeviceAssignmentTable,
    ApplicationSetVirtualDeviceContextAssignmentTable,
    SecurityZoneDeviceAssignmentTable,
    SecurityZoneVirtualDeviceContextAssignmentTable,
    SecurityZoneInterfaceAssignmentTable,
    AddressDeviceAssignmentTable,
    AddressVirtualDeviceContextAssignmentTable,
    AddressSetDeviceAssignmentTable,
    AddressSetVirtualDeviceContextAssignmentTable,
    AddressListAddressTable,
    AddressListAddressSetTable,
    FirewallFilterDeviceAssignmentTable,
    FirewallFilterVirtualDeviceContextAssignmentTable,
    PolicerDeviceAssignmentTable,
    PolicerVirtualDeviceContextAssignmentTable,
)


class AddressContextInfo(PluginTemplateExtension):
    models = ["netbox_security.address"]

    def right_page(self):
        """ """
        if self.context["config"].get("address_ext_page") == "right":
            return self.x_page()
        return ""

    def left_page(self):
        """ """
        if self.context["config"].get("address_ext_page") == "left":
            return self.x_page()
        return ""

    def full_width_page(self):
        """ """
        if self.context["config"].get("address_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        obj = self.context["object"]
        address_lists = AddressList.objects.filter(address=obj)
        address_table = AddressListAddressTable(address_lists)
        return self.render(
            "netbox_security/address/extend.html",
            extra_context={"related_address_table": address_table},
        )


class AddressSetContextInfo(PluginTemplateExtension):
    models = ["netbox_security.addressset"]

    def right_page(self):
        """ """
        if self.context["config"].get("address_ext_page") == "right":
            return self.x_page()
        return ""

    def left_page(self):
        """ """
        if self.context["config"].get("address_ext_page") == "left":
            return self.x_page()
        return ""

    def full_width_page(self):
        """ """
        if self.context["config"].get("address_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        obj = self.context["object"]
        address_lists = AddressList.objects.filter(address_set=obj)
        address_table = AddressListAddressSetTable(address_lists)
        return self.render(
            "netbox_security/address/extend.html",
            extra_context={"related_address_table": address_table},
        )


class VirtualDeviceContextInfo(PluginTemplateExtension):
    models = ["dcim.virtualdevicecontext"]

    def right_page(self):
        """ """
        if self.context["config"].get("virtual_ext_page") == "right":
            return self.x_page()
        return ""

    def left_page(self):
        """ """
        if self.context["config"].get("virtual_ext_page") == "left":
            return self.x_page()
        return ""

    def full_width_page(self):
        """ """
        if self.context["config"].get("virtual_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        obj = self.context["object"]
        pool_assignments = NatPoolAssignment.objects.filter(virtualdevicecontext=obj)
        pool_table = NatPoolVirtualDeviceContextAssignmentTable(pool_assignments)
        ruleset_assignments = NatRuleSetAssignment.objects.filter(
            virtualdevicecontext=obj
        )
        ruleset_table = NatRuleSetVirtualDeviceContextAssignmentTable(
            ruleset_assignments
        )
        zone_assignments = SecurityZoneAssignment.objects.filter(
            virtualdevicecontext=obj
        )
        zone_table = SecurityZoneVirtualDeviceContextAssignmentTable(zone_assignments)
        address_assignments = AddressAssignment.objects.filter(virtualdevicecontext=obj)
        address_table = AddressVirtualDeviceContextAssignmentTable(address_assignments)
        addressset_assignments = AddressSetAssignment.objects.filter(
            virtualdevicecontext=obj
        )
        addressset_table = AddressSetVirtualDeviceContextAssignmentTable(
            addressset_assignments
        )
        firewall_filter_assignments = FirewallFilterAssignment.objects.filter(
            virtualdevicecontext=obj
        )
        firewall_filter_table = FirewallFilterVirtualDeviceContextAssignmentTable(
            firewall_filter_assignments
        )
        policer_assignments = PolicerAssignment.objects.filter(virtualdevicecontext=obj)
        policer_table = PolicerVirtualDeviceContextAssignmentTable(policer_assignments)
        application_assignments = ApplicationAssignment.objects.filter(
            virtualdevicecontext=obj
        )
        application_table = ApplicationVirtualDeviceContextAssignmentTable(
            application_assignments
        )
        application_set_assignments = ApplicationSetAssignment.objects.filter(
            virtualdevicecontext=obj
        )
        application_set_table = ApplicationSetVirtualDeviceContextAssignmentTable(
            application_set_assignments
        )
        return self.render(
            "netbox_security/device/device_extend.html",
            extra_context={
                "related_pool_table": pool_table,
                "related_ruleset_table": ruleset_table,
                "related_zone_table": zone_table,
                "related_address_table": address_table,
                "related_addressset_table": addressset_table,
                "related_firewall_filter_table": firewall_filter_table,
                "related_firewall_policer_table": policer_table,
                "related_application_table": application_table,
                "related_application_set_table": application_set_table,
            },
        )


class VirtualMachineInfo(PluginTemplateExtension):
    models = ["virtualization.virtualmachine"]

    def right_page(self):
        """ """
        if self.context["config"].get("virtual_ext_page") == "right":
            return self.x_page()
        return ""

    def left_page(self):
        """ """
        if self.context["config"].get("virtual_ext_page") == "left":
            return self.x_page()
        return ""

    def full_width_page(self):
        """ """
        if self.context["config"].get("virtual_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        obj = self.context["object"]
        pool_assignments = NatPoolAssignment.objects.filter(virtualmachine=obj)
        pool_table = NatPoolVirtualMachineAssignmentTable(pool_assignments)
        ruleset_assignments = NatRuleSetAssignment.objects.filter(virtualmachine=obj)
        ruleset_table = NatRuleSetVirtualMachineAssignmentTable(ruleset_assignments)
        return self.render(
            "netbox_security/virtualmachine/virtualmachine_extend.html",
            extra_context={
                "related_pool_table": pool_table,
                "related_ruleset_table": ruleset_table,
            },
        )


class DeviceInfo(PluginTemplateExtension):
    models = ["dcim.device"]

    def right_page(self):
        """ """
        if self.context["config"].get("device_ext_page") == "right":
            return self.x_page()
        return ""

    def left_page(self):
        """ """
        if self.context["config"].get("device_ext_page") == "left":
            return self.x_page()
        return ""

    def full_width_page(self):
        """ """
        if self.context["config"].get("device_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        obj = self.context["object"]
        pool_assignments = NatPoolAssignment.objects.filter(device=obj)
        pool_table = NatPoolDeviceAssignmentTable(pool_assignments)
        ruleset_assignments = NatRuleSetAssignment.objects.filter(device=obj)
        ruleset_table = NatRuleSetDeviceAssignmentTable(ruleset_assignments)
        zone_assignments = SecurityZoneAssignment.objects.filter(device=obj)
        zone_table = SecurityZoneDeviceAssignmentTable(zone_assignments)
        address_assignments = AddressAssignment.objects.filter(device=obj)
        address_table = AddressDeviceAssignmentTable(address_assignments)
        addressset_assignments = AddressSetAssignment.objects.filter(device=obj)
        addressset_table = AddressSetDeviceAssignmentTable(addressset_assignments)
        firewall_filter_assignments = FirewallFilterAssignment.objects.filter(
            device=obj
        )
        firewall_filter_table = FirewallFilterDeviceAssignmentTable(
            firewall_filter_assignments
        )
        policer_assignments = PolicerAssignment.objects.filter(device=obj)
        policer_table = PolicerDeviceAssignmentTable(policer_assignments)
        application_assignments = ApplicationAssignment.objects.filter(device=obj)
        application_table = ApplicationDeviceAssignmentTable(application_assignments)
        application_set_assignments = ApplicationSetAssignment.objects.filter(
            device=obj
        )
        application_set_table = ApplicationSetDeviceAssignmentTable(
            application_set_assignments
        )
        return self.render(
            "netbox_security/device/device_extend.html",
            extra_context={
                "related_pool_table": pool_table,
                "related_ruleset_table": ruleset_table,
                "related_zone_table": zone_table,
                "related_address_table": address_table,
                "related_addressset_table": addressset_table,
                "related_firewall_filter_table": firewall_filter_table,
                "related_firewall_policer_table": policer_table,
                "related_application_table": application_table,
                "related_application_set_table": application_set_table,
            },
        )


class InterfaceInfo(PluginTemplateExtension):
    models = ["dcim.interface"]

    def right_page(self):
        """ """
        if self.context["config"].get("interface_ext_page") == "right":
            return self.x_page()
        return ""

    def left_page(self):
        """ """
        if self.context["config"].get("interface_ext_page") == "left":
            return self.x_page()
        return ""

    def full_width_page(self):
        """ """
        if self.context["config"].get("interface_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        """ """
        obj = self.context["object"]
        rule_assignments = NatRuleAssignment.objects.filter(interface=obj)
        rule_table = NatRuleAssignmentTable(rule_assignments)
        zone_assignments = SecurityZoneAssignment.objects.filter(interface=obj)
        zone_table = SecurityZoneInterfaceAssignmentTable(zone_assignments)
        return self.render(
            "netbox_security/interface/interface_extend.html",
            extra_context={
                "related_rule_table": rule_table,
                "related_zone_table": zone_table,
            },
        )


template_extensions = [
    AddressContextInfo,
    AddressSetContextInfo,
    VirtualDeviceContextInfo,
    VirtualMachineInfo,
    DeviceInfo,
    InterfaceInfo,
]
