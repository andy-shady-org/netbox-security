from netbox.plugins import PluginTemplateExtension


class SecurityZoneContextInfo(PluginTemplateExtension):
    models = ["netbox_security.securityzone"]

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
        return self.render(
            "netbox_security/securityzone/extend.html",
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
        return self.render(
            "netbox_security/address/extend.html",
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
        return self.render(
            "netbox_security/addressset/extend.html",
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
        return self.render(
            "netbox_security/virtualmachine/virtualmachine_extend.html",
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
        return self.render(
            "netbox_security/interface/interface_extend.html",
        )


template_extensions = [
    SecurityZoneContextInfo,
    AddressContextInfo,
    AddressSetContextInfo,
    VirtualMachineInfo,
    InterfaceInfo,
]
