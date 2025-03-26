from netbox.plugins import PluginTemplateExtension

from netbox_security.models import (
    NatPoolAssignment,
    NatRuleSetAssignment,
    NatRuleAssignment,
    SecurityZoneAssignment,
    AddressAssignment,
)
from netbox_security.tables import (
    NatPoolDeviceAssignmentTable,
    NatPoolVirtualDeviceContextAssignmentTable,
    NatRuleSetDeviceAssignmentTable,
    NatRuleSetVirtualDeviceContextAssignmentTable,
    NatRuleAssignmentTable,
    SecurityZoneDeviceAssignmentTable,
    SecurityZoneVirtualDeviceContextAssignmentTable,
    SecurityZoneInterfaceAssignmentTable,
    AddressDeviceAssignmentTable,
    AddressVirtualDeviceContextAssignmentTable,
)


class VirtualDeviceContextInfo(PluginTemplateExtension):
    model = 'dcim.virtualdevicecontext'

    def right_page(self):
        """
        """
        if self.context['config'].get('virtual_ext_page') == 'right':
            return self.x_page()
        return ''

    def left_page(self):
        """
        """
        if self.context['config'].get('virtual_ext_page') == 'left':
            return self.x_page()
        return ''

    def full_width_page(self):
        """
        """
        if self.context['config'].get('virtual_ext_page') == 'full_width':
            return self.x_page()
        return ''

    def x_page(self):
        obj = self.context['object']
        pool_assignments = NatPoolAssignment.objects.filter(virtualdevicecontext=obj)
        pool_table = NatPoolVirtualDeviceContextAssignmentTable(pool_assignments)
        ruleset_assignments = NatRuleSetAssignment.objects.filter(virtualdevicecontext=obj)
        ruleset_table = NatRuleSetVirtualDeviceContextAssignmentTable(ruleset_assignments)
        zone_assignments = SecurityZoneAssignment.objects.filter(virtualdevicecontext=obj)
        zone_table = SecurityZoneVirtualDeviceContextAssignmentTable(zone_assignments)
        address_assignments = AddressAssignment.objects.filter(virtualdevicecontext=obj)
        address_table = AddressVirtualDeviceContextAssignmentTable(address_assignments)
        return self.render(
            'netbox_security/device/device_extend.html',
            extra_context={
                'related_pool_table': pool_table,
                'related_ruleset_table': ruleset_table,
                'related_zone_table': zone_table,
                'related_address_table': address_table,
            }
        )


class DeviceInfo(PluginTemplateExtension):
    model = 'dcim.device'

    def right_page(self):
        """
        """
        if self.context['config'].get('device_ext_page') == 'right':
            return self.x_page()
        return ''

    def left_page(self):
        """
        """
        if self.context['config'].get('device_ext_page') == 'left':
            return self.x_page()
        return ''

    def full_width_page(self):
        """
        """
        if self.context['config'].get('device_ext_page') == 'full_width':
            return self.x_page()
        return ''

    def x_page(self):
        obj = self.context['object']
        pool_assignments = NatPoolAssignment.objects.filter(device=obj)
        pool_table = NatPoolDeviceAssignmentTable(pool_assignments)
        ruleset_assignments = NatRuleSetAssignment.objects.filter(device=obj)
        ruleset_table = NatRuleSetDeviceAssignmentTable(ruleset_assignments)
        zone_assignments = SecurityZoneAssignment.objects.filter(device=obj)
        zone_table = SecurityZoneDeviceAssignmentTable(zone_assignments)
        address_assignments = AddressAssignment.objects.filter(device=obj)
        address_table = AddressDeviceAssignmentTable(address_assignments)
        return self.render(
            'netbox_security/device/device_extend.html',
            extra_context={
                'related_pool_table': pool_table,
                'related_ruleset_table': ruleset_table,
                'related_zone_table': zone_table,
                'related_address_table': address_table,
            }
        )


class InterfaceInfo(PluginTemplateExtension):
    model = 'dcim.interface'

    def right_page(self):
        """
        """
        if self.context['config'].get('interface_ext_page') == 'right':
            return self.x_page()
        return ''

    def left_page(self):
        """
        """
        if self.context['config'].get('interface_ext_page') == 'left':
            return self.x_page()
        return ''

    def full_width_page(self):
        """
        """
        if self.context['config'].get('interface_ext_page') == 'full_width':
            return self.x_page()
        return ''

    def x_page(self):
        """
        """
        obj = self.context['object']
        rule_assignments = NatRuleAssignment.objects.filter(interface=obj)
        rule_table = NatRuleAssignmentTable(rule_assignments)
        zone_assignments = SecurityZoneAssignment.objects.filter(interface=obj)
        zone_table = SecurityZoneInterfaceAssignmentTable(zone_assignments)
        return self.render(
            'netbox_security/interface/interface_extend.html',
            extra_context={
                            'related_rule_table': rule_table,
                            'related_zone_table': zone_table,
            }
        )


template_extensions = [VirtualDeviceContextInfo, DeviceInfo, InterfaceInfo]
